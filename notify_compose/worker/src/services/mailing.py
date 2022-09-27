from functools import lru_cache
from typing import Optional, Type

from providers.mailing import get_mailing_client
from services.mailing_client import AbstractMailingClient, BaseMailingClient


@lru_cache()
async def get_mailing_service(
        mailing_client: Optional[Type[AbstractMailingClient]] = None
):
    mailing_client = await get_mailing_client() if mailing_client is None else mailing_client
    return BaseMailingClient(client=mailing_client)  # type: ignore
