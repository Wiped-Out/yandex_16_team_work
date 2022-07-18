import os

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

    POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)

    API_URL = os.getenv('API_URL', 'http://flask:5000')

    TABLES_NAMES_MAPPINGS = {
        "users": "testdata/sql_tables/users.sql",
        "roles": "testdata/sql_tables/roles.sql",
    }

    class Config:
        env_file = ".env"


settings = Settings()
