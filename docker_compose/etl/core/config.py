from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


class Settings(BaseSettings):
    ELASTIC_URI: str


class PostgresDSL(BaseSettings):
    dbname: str = Field(env='DB_NAME')
    user: str = Field(env='DB_USER')
    password: str = Field(env='DB_PASSWORD')
    host: str = Field(env='127.0.0.1')
    port: int = Field(env='DB_PORT')


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

postgres_dsl = PostgresDSL()
