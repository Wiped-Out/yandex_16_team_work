from typing import Optional

from services.mailing_client import AbstractMailingClient

mailing_client: Optional[AbstractMailingClient] = None


# Функция понадобится при внедрении зависимостей
async def get_mailing_client() -> AbstractMailingClient:
    if not mailing_client:
        raise
    return mailing_client
