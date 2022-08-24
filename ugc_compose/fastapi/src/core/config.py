import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str
    AUTH_SERVICE_URL: str
    JWT_PUBLIC_KEY: str
    NO_JWT: bool

    KAFKA_HOST: str
    KAFKA_PORT: int

    LOGSTASH_HOST: str
    LOGSTASH_PORT: int
    ENABLE_LOGSTASH: bool

    SENTRY_DSN: str
    ENABLE_SENTRY: bool

    class Config:
        env_file = ".env"


# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings = Settings()
