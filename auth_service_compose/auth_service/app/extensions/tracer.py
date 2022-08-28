import contextlib
from functools import wraps
from typing import Optional

from core.settings import settings
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

Instrumentor: Optional[FlaskInstrumentor] = None


def configure_tracer() -> None:
    if not settings.ENABLE_TRACER:
        return

    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create(
                {SERVICE_NAME: 'auth_service'},
            ),
        ),
    )

    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=settings.JAEGER_HOST,
                agent_port=settings.JAEGER_PORT,
            ),
        ),
    )


def _trace():
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if not settings.ENABLE_TRACER:
                return func(*args, **kwargs)

            with contextlib.suppress(OSError):
                tracer = trace.get_tracer(__name__)
                with tracer.start_as_current_span(func.__name__):
                    return func(*args, **kwargs)

        return inner

    return func_wrapper
