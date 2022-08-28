import os
from logging import config as logging_config

from core.logger import LOGGING
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    PROJECT_NAME: str
    REDIS_HOST: str
    REDIS_PORT: int
    ELASTIC_HOST: str
    ELASTIC_PORT: int
    AUTH_SERVICE_URL: str
    JWT_PUBLIC_KEY: str
    NO_JWT = os.getenv('NO_JWT', False) == 'True'

    class Config:
        env_file = '.env'


# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings = Settings()
