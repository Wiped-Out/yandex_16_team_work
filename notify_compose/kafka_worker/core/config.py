import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    KAFKA_HOST: str
    KAFKA_PORT: int

    TOPICS_NAMES: list
    NOTIFY_API_ENDPOINT: str

    EMAIL_CONFIRMATION_TEMPLATE_UUID: str
    PASSWORD_GENERATION_TEMPLATE_UUID: str

    class Config:
        env_file = '.env'


class JWTBearerUser(BaseSettings):
    REFRESH_URL: str

    TOKEN: str
    REFRESH_TOKEN: str

    class Config:
        env_file = '.env'


# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

user = JWTBearerUser().dict()
