import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str
    AUTH_SERVICE_URL: str
    JWT_PUBLIC_KEY: str
    NO_JWT: bool

    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_DB_NAME: str

    RABBIT_HOST: str
    RABBIT_PORT: int
    RABBIT_USER: str
    RABBIT_PASSWORD: str
    RABBIT_MAX_PRIORITY: int

    LOGSTASH_HOST: str
    LOGSTASH_PORT: int
    ENABLE_LOGSTASH: bool

    SENTRY_DSN: str
    ENABLE_SENTRY: bool

    class Config:
        env_file = '.env'


# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
