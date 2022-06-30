import os

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
    ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))
    API_URL = os.getenv('API_URL', 'http://127.0.0.1')

    class Config:
        env_file = ".env"

settings = Settings()