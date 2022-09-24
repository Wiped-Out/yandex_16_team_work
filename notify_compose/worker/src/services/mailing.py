from models.models import EmailMessage
from services.mailing_client import BaseMailingClient


class MailingService(BaseMailingClient):
    async def send_email(self, messages: list[EmailMessage]):
        await self.send(messages=messages)
