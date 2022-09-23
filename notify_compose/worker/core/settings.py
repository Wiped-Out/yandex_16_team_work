import os
from pydantic import BaseSettings


class Settings(BaseSettings):
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
