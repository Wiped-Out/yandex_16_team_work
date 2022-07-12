import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5432))
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'db')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'user')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')

    class Config:
        env_file = ".env"


# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings = Settings()
