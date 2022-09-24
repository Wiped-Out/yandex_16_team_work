from abc import ABC, abstractmethod

from mailjet_rest import Client
from models.models import EmailMessage


class AbstractMailingClient(ABC):
    @abstractmethod
    async def send_email(self, messages: list[EmailMessage]) -> int:
        pass


class MailJetMailingClient(AbstractMailingClient):
    def __init__(self, client: Client):
        self.client = client

    async def send_email(self, messages: list[EmailMessage]) -> int:
        mailing_service_response = self.client.send.create(
            data={"Messages": [message.dict() for message in messages]},
        )
        return mailing_service_response.status_code


class BaseMailingClient:
    def __init__(self, client: AbstractMailingClient):
        self.client = client

    async def send(self, messages: list[EmailMessage]) -> int:
        return await self.client.send_email(messages=messages)
