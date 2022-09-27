from functools import lru_cache

from dotenv import load_dotenv
from pydantic import UUID4, BaseSettings

load_dotenv()


class Settings(BaseSettings):
    NOTIFY_API_ENDPOINT: str
    PROLONG_SUBSCRIPTION_TEMPLATE_UUID: UUID4

    USER_IDS: list[UUID4]

    class Config:
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == 'USER_IDS':
                return [x for x in raw_val.split(',') if x]
            return cls.json_loads(raw_val)  # type: ignore


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
