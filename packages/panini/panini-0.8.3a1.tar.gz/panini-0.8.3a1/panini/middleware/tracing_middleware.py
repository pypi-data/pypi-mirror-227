try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider, Tracer
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.resources import SERVICE_NAME, Resource
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
except ImportError:
    raise Exception("Tracing dependencies not found, try to run `$ pip install panini[tracing]`")
import inspect
import uuid
import json
from functools import wraps
from typing import Optional
from nats.aio.msg import Msg
from panini.app import get_app
from dataclasses import dataclass
from panini.middleware import Middleware
from panini.managers.event_manager import Listen
import warnings


@dataclass
class SpanConfig:
    """
     Represents a configuration for a span.
    Attributes:
        span_name (str): The name of the span.
        span_attributes (Optional[dict]): The optional dictionary of attributes for the span.
    """
    span_name: str
    span_attributes: Optional[dict]


def register_trace(**decorator_kwargs):  # the decorator
    def wrapper(f):  # a wrapper for the function
        if inspect.iscoroutinefunction(f):
            @wraps(f)
            async def decorated_function(*args, **kwargs):  # the decorated function
                ctx = trace.get_current_span().get_span_context()
                link = trace.Link(ctx)
                _tracer = trace.get_tracer(__name__)
                with _tracer.start_as_current_span(decorator_kwargs.get("span_name", f"unknown-{uuid.uuid4().hex}"),
                                                   links=[link]):
                    result = await f(*args, **kwargs)
                return result
        else:
            @wraps(f)
            def decorated_function(*args, **kwargs):  # the decorated function
                ctx = trace.get_current_span().get_span_context()
                link = trace.Link(ctx)
                _tracer = trace.get_tracer(__name__)
                with _tracer.start_as_current_span(decorator_kwargs.get("span_name", f"unknown-{uuid.uuid4().hex}"),
                                                   links=[link]):
                    result = f(*args, **kwargs)
                return result

        return decorated_function

    return wrapper


class OTELTracer:
    """
    The OTELTracer class is used to create and configure an OpenTelemetry tracer for distributed tracing.
    Attributes:
        tracing_config (dict): The configuration dictionary containing the tracing settings.
        service_name (str): The name of the service being traced.
        _config (dict): The internal configuration dictionary.
        _exporter_config (dict): The configuration for the tracer exporter.
        _provider_config (dict): The configuration for the tracer provider.
        _custom_config (dict): Additional custom configuration provided by the user.
        tracer: The OpenTelemetry tracer instance.
    Methods:
        __init__(self, tracing_config: dict, **kwargs)
            Initializes a new instance of the OTELTracer class.
            Args:
                tracing_config (dict): The configuration dictionary containing the tracing settings.
                **kwargs: Additional custom configuration parameters.
        create_tracer(self)
            Creates and configures the OpenTelemetry tracer.
            Returns:
                The initialized OpenTelemetry tracer instance.
    """

    def __init__(self, tracing_config: dict, **kwargs):
        self._config = tracing_config
        self.service_name = self._config["service_name"]
        self._exporter_config = self._config["exporter_config"]
        self._provider_config = self._config["provider_config"]
        self._custom_config = self._config["custom_config"]
        self._custom_config.update(**kwargs)
        self.tracer = self.create_tracer()

    def create_tracer(self):
        resource = Resource(attributes={
            SERVICE_NAME: self.service_name
        })
        provider = TracerProvider(resource=resource, **self._provider_config)
        processor = BatchSpanProcessor(OTLPSpanExporter(**self._exporter_config))
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        return trace.get_tracer(__name__)


class TracingMiddleware(Middleware):
    """
    Class representing a middleware for tracing requests and events in a Panini application.
    Args:
        tracing_config (dict): A dictionary containing the configuration parameters for tracing.
    Attributes:
        _otel_tracer (OTELTracer): The OpenTelemetry Tracer instance.
        tracer (Tracer): The Tracer instance extracted from _otel_tracer.
        parent (TraceContextTextMapPropagator): The Trace Context TextMap Propagator instance.
    Methods:
        _create_uuid(): Generates a UUID v4 string.
        send_any(subject: str, message: Msg, send_func, *args, **kwargs): Sends a message with tracing information.
        wildcard_match(match_key: str, subject: str) -> str: Performs a wildcard match between two strings.
        listen_any(msg: Msg, callback): Listens for events with tracing information.
    """

    def __init__(
            self,
            tracing_config: dict,
            **kwargs
    ):
        self._otel_tracer = OTELTracer(tracing_config=tracing_config, **kwargs)
        self.tracer: Tracer = self._otel_tracer.tracer
        self.parent = TraceContextTextMapPropagator()
        super().__init__()

    def _create_uuid(self) -> str:
        return uuid.uuid4().hex

    async def send_any(self, subject: str, message: Msg, send_func, *args, **kwargs):
        carrier = {}
        headers = {}
        span_config = kwargs.get("span_config")
        use_tracing = kwargs.get("use_tracing", True)
        if kwargs.get("use_current_span", False):
            ctx = trace.get_current_span().get_span_context()
            link = [trace.Link(ctx)]
        else:
            link = []
        if not isinstance(span_config, SpanConfig):
            span_config = SpanConfig(
                span_name=self._create_uuid(),
                span_attributes={})
        if use_tracing is True and span_config:
            with self.tracer.start_as_current_span(span_config.span_name, links=link) as span:
                for attr_key, attr_value in span_config.span_attributes.items():
                    span.set_attribute(attr_key, attr_value)
                self.parent.inject(carrier=carrier)
                headers = {
                    "tracing_span_name": span_config.span_name,
                    "tracing_span_carrier": json.dumps(carrier)
                }
        if "use_tracing" in kwargs:
            del kwargs['use_tracing']
        response = await send_func(subject, message, headers=headers)
        return response

    @classmethod
    def wildcard_match(cls, match_key: str, subject: str) -> Optional[str]:
        """Perform a wildcard match between the match_key and the subject"""
        split_subject = subject.split('.')
        split_key = match_key.split('.')

        # if `>` at the end of match_key
        if split_key[-1] == '>':
            if len(split_subject) < len(split_key) - 1:  # -1 because `>` matches remaining parts
                return None
            # checking parts before `>` match
            for k, s in zip(split_key[:-1], split_subject):
                if k != "*" and k != s:
                    return None
            # parts before `>` matched in both
            return match_key

        # if not `>` at the end
        if len(split_subject) != len(split_key):
            return None

        if all(k == "*" or k == s for k, s in zip(split_key, split_subject)):
            return match_key

        return None

    async def listen_any(self, msg: Msg, callback):
        context = {}
        app = get_app()
        assert app is not None
        for subject in app._event_manager.subscriptions.keys():
            matched_subject = self.wildcard_match(subject, msg.subject)
            if not matched_subject:
                continue
            listen_obj_list = app._event_manager.subscriptions[matched_subject]
            listen_object: Listen
            for listen_object in listen_obj_list:
                use_tracing = listen_object._meta.get("use_tracing", True)
                if use_tracing:
                    if id(callback) == id(
                            listen_object.callback) and callback.__name__ == listen_object.callback.__name__:
                        headers = msg.headers
                        if headers:
                            context = self.parent.extract(
                                carrier=json.loads(msg.headers.get("tracing_span_carrier", "{}")))
                        span_config = listen_object._meta.get("span_config")
                        if not isinstance(span_config, SpanConfig):
                            span_config = SpanConfig(
                                span_name=self._create_uuid(),
                                span_attributes={})
                        with self.tracer.start_as_current_span(span_config.span_name, context=context) as span:
                            for attr_key, attr_val in span_config.span_attributes.items():
                                span.set_attribute(attr_key, attr_val)
                            response = await callback(msg)
                            return response
                    else:
                        warnings.warn(
                            "TracingMiddleware logic on listener doesn't work, it should be placed first when adding middlewares!")
                        return await callback(msg)
        return await callback(msg)
