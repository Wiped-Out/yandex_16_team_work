from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):

    KAFKA_HOSTNAME: str = 'localhost'
    KAFKA_PORT: str = '29092'
    MAX_WAITING_TIME: int = 0

    MAX_NUMBER_FILMS: int = 10000
    MAX_NUMBER_USERS: int = 10000

    class Config:
        env_file = '.env'


settings = Settings()
