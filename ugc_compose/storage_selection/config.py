from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    MAX_WAITING_TIME: int = 0

    MAX_NUMBER_FILMS: int = 100000
    MAX_NUMBER_USERS: int = 100000

    MONGODB_HOST: str
    MONGODB_PORT: int

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
