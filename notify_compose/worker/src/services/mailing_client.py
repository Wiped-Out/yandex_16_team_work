from abc import ABC, abstractmethod
from typing import Union

from core.config import settings
from dotwiz import DotWiz
from mailjet_rest import Client
from models.models import (EmailMessage, EmailReceiver, EmailSender, Template,
                           TemplateTypeEnum)


class AbstractMailingClient(ABC):
    @abstractmethod
    async def send(self, ready_template: str, template: Template, user: Union[dict, DotWiz]) -> int:
        pass


class MailJetMailingClient(AbstractMailingClient):
    def __init__(self, client: Client):
        self.client = client

    async def send(self, ready_template: str, template: Template, user: Union[dict, DotWiz]) -> int:
        message = EmailMessage(
            From=EmailSender(
                Email=settings.SENDER_EMAIL,
                Name=settings.SENDER_NAME
            ),
            To=[EmailReceiver(
                Email=user['email'],
                Name=user['login']
            )],
            Subject=template.subject,
            TextPart=ready_template if template.template_type is TemplateTypeEnum.plain else "",
            HTMLPart=ready_template if template.template_type is TemplateTypeEnum.html else ""
        )

        mailing_service_response = self.client.send.create(
            data={"Messages": [message.dict()]},
        )
        return mailing_service_response.status_code


class BaseMailingClient:
    def __init__(self, client: AbstractMailingClient):
        self.client = client

    async def send(self, ready_template: str, template: Template, user: Union[dict, DotWiz]) -> int:
        return await self.client.send(ready_template,
                                      template,
                                      user)
