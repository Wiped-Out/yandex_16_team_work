from models.models import EmailSender, EmailReceiver, EmailMessage
from services.mailing_client import BaseMailingClient


class MailingService(BaseMailingClient):
    async def send_email(self, messages: list[EmailMessage]):
        await self.send(messages=messages)

    async def build_message(
            self,
            sender: EmailSender,
            receivers: list[EmailReceiver],
            subject: str,
            text: str,
            html: str,
    ) -> EmailMessage:
        return EmailMessage(
            From=sender,
            To=receivers,
            Subject=subject,
            TextPart=text,
            HTMLPart=html,
        )

    async def build_sender(self, sender_email: str, sender_name: str) -> EmailSender:
        return EmailSender(Email=sender_email, Name=sender_name)

    async def build_receiver(self, receiver_email: str, receiver_name: str) -> EmailReceiver:
        return EmailReceiver(Email=receiver_email, Name=receiver_name)
