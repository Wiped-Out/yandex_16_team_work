import os
from logging import config as logging_config
from dotenv import load_dotenv
from pydantic import BaseSettings

from core.logger import LOGGING

load_dotenv()

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')
    REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
    ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))

    class Config:
        env_file = ".env"


# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings = Settings()
