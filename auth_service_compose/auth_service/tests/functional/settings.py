from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int

    POSTGRES_DB_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    API_URL: str

    TABLES_NAMES_MAPPINGS = {
        "users": "testdata/sql_tables/users.sql",
        "roles": "testdata/sql_tables/roles.sql",
        "user_roles": "testdata/sql_tables/user_roles.sql",
    }

    class Config:
        env_file = ".env"


settings = Settings()
