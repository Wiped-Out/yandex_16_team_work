from pydantic import BaseSettings, Field
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    ELASTIC_URI: str


class PostgresDSL(BaseSettings):
    dbname: str = Field(env='DB_NAME')
    user: str = Field(env='DB_USER')
    password: str = Field(env='DB_PASSWORD')
    host: str = Field(env='127.0.0.1')
    port: int = Field(env='DB_PORT')


settings = Settings()

postgres_dsl = PostgresDSL()
