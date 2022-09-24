from datetime import datetime
from enum import Enum
from uuid import uuid4

from models.base import BaseOrjsonModel
from pydantic import UUID4, Field


class TemplateTypeEnum(str, Enum):
    html = 'html'
    plain = 'plain'


class NotificationTypeEnum(str, Enum):
    email = 'email'


class NotificationStatusEnum(str, Enum):
    created = 'created'
    in_progress = 'in_progress'
    failed = 'failed'
    finished = 'finished'


class HTTPTypeEnum(str, Enum):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'


class Notification(BaseOrjsonModel):
    id: UUID4 = Field(default_factory=uuid4)
    template_id: UUID4
    priority: int
    notification_type: NotificationTypeEnum
    user_ids: list[UUID4]
    status: NotificationStatusEnum
    created_at: datetime = Field(default_factory=datetime.utcnow)
    before: datetime


class TemplateFieldItem(BaseOrjsonModel):
    name: str
    url: str
    body: dict
    headers: dict
    fetch_pattern: str
    http_type: HTTPTypeEnum


class Template(BaseOrjsonModel):
    id: UUID4 = Field(default_factory=uuid4)
    body: str
    template_type: TemplateTypeEnum
    fields: list[TemplateFieldItem]


class EmailSender(BaseOrjsonModel):
    Email: str
    Name: str


class EmailReceiver(BaseOrjsonModel):
    Email: str
    Name: str


class EmailMessage(BaseOrjsonModel):
    From: EmailSender
    To: list[EmailReceiver]
    Subject: str
    TextPart: str
    HTMLPart: str
