import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

from core.config import settings


def init_sentry():
    if not settings.ENABLE_SENTRY:
        return
    sentry_sdk.init(dsn=settings.SENTRY_DSN,
                    integrations=[FastApiIntegration()])
