from enum import Enum

from models.base import BaseOrjsonModel
from datetime import datetime
from uuid import uuid4
from pydantic import Field, UUID4


class TemplateTypeEnum(str, Enum):
    html = 'html'
    plain = 'plain'


class NotificationTypeEnum(str, Enum):
    email = 'email'


class HTTPTypeEnum(str, Enum):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'


class Notification(BaseOrjsonModel):
    id: UUID4 = Field(default_factory=uuid4)
    template_id: UUID4
    priority: int
    notification_type: str
    user_ids: list[UUID4]
    status: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    before: datetime = Field(default_factory=datetime.utcnow)


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
