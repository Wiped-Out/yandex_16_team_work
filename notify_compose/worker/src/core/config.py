import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    MAILJET_API_KEY: str
    MAILJET_SECRET_KEY: str

    RABBIT_HOST: str
    RABBIT_PORT: int
    RABBIT_USER: str
    RABBIT_PASSWORD: str
    RABBIT_MAX_PRIORITY: int
    RABBIT_QUEUE_NAME: str = 'email'

    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_DB_NAME: str
    NOTIFICATIONS_COLLECTION: str = 'notifications'
    TEMPLATES_COLLECTION: str = 'templates'

    SENDER_EMAIL: str = 'noreply@film-service.com'
    SENDER_NAME: str = 'Super-puper Film-service'

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
