from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Type, Optional, Union

from dotwiz import DotWiz
from mailjet_rest import Client

from core.config import settings
from models.models import EmailMessage, Template, EmailReceiver, EmailSender, TemplateTypeEnum
from providers.mailing import get_mailing_client


class AbstractMailingClient(ABC):
    @abstractmethod
    async def send_email(self, ready_template: str, template: Template, user: Union[dict, DotWiz]) -> int:
        pass


class MailJetMailingClient(AbstractMailingClient):
    def __init__(self, client: Client):
        self.client = client

    async def send_email(self, ready_template: str, template: Template, user: Union[dict, DotWiz]) -> int:
        message = EmailMessage(
            From=EmailSender(
                Email=settings.SENDER_EMAIL,
                Name=settings.SENDER_NAME
            ),
            To=EmailReceiver(
                Email=user['email'],
                Name=user['login']
            ),
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
        return await self.client.send_email(ready_template=ready_template,
                                            template=template,
                                            user=user)


@lru_cache()
def get_mailing_service(
        mailing_client: Optional[Type[AbstractMailingClient]] = None
):
    mailing_client = get_mailing_client() if mailing_client is None else mailing_client
    return BaseMailingClient(client=mailing_client)  # type: ignore
