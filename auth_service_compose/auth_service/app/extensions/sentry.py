import sentry_sdk
from core.settings import settings
from sentry_sdk.integrations.flask import FlaskIntegration


def init_sentry():
    if not settings.ENABLE_SENTRY:
        return
    sentry_sdk.init(dsn=settings.SENTRY_DSN,
                    integrations=[FlaskIntegration()])
