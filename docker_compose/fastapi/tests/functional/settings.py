from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    ELASTIC_HOST: str
    ELASTIC_PORT: int
    API_URL: str

    INDEXES_NAMES_MAPPINGS = {
        "movies": "testdata/indexes_mapping/movies.json",
        "persons": "testdata/indexes_mapping/persons.json",
        "genres": "testdata/indexes_mapping/genres.json",
    }

    class Config:
        env_file = ".env"


settings = Settings()
