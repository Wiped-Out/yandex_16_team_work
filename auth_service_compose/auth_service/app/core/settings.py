import os
from datetime import timedelta

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    JAEGER_HOST: str
    JAEGER_PORT: int

    REQUEST_LIMIT_PER_MINUTE: int

    API_URL: str

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=2)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_SECRET_KEY: str
    JWT_PUBLIC_KEY: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    ENABLE_LIMITER: bool
    ENABLE_TRACER: bool

    class Config:
        env_file = '.env'


# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings = Settings()
