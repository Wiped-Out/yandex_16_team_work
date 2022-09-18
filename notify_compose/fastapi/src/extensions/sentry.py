import sentry_sdk
from core.config import settings
from sentry_sdk.integrations.fastapi import FastApiIntegration


def init_sentry():
    if not settings.ENABLE_SENTRY:
        return
    sentry_sdk.init(dsn=settings.SENTRY_DSN,
                    integrations=[FastApiIntegration()])
