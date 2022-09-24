import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    MAILJET_API_KEY: str
    MAILJET_SECRET_KEY: str

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

settings = Settings()
user = JWTBearerUser()
