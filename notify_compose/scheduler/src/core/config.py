from pydantic import BaseSettings, UUID4
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    NOTIFY_API_ENDPOINT: str
    TEMPLATE_UUID: UUID4


settings = Settings()
