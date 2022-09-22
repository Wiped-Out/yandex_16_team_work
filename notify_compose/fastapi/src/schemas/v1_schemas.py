from datetime import datetime

from pydantic import BaseModel
from pydantic.types import UUID4

from models.models import NotificationTypeEnum, TemplateTypeEnum, HTTPTypeEnum, NotificationStatusEnum


class Created(BaseModel):
    id: UUID4


class TemplateFieldItem(BaseModel):
    name: str
    url: str
    body: dict
    headers: dict
    fetch_pattern: str
    http_type: HTTPTypeEnum


class Template(BaseModel):
    id: UUID4
    body: str
    template_type: TemplateTypeEnum
    fields: list[TemplateFieldItem]


class Notification(BaseModel):
    id: UUID4
    template_id: UUID4
    priority: int
    notification_type: NotificationTypeEnum
    user_ids: list[UUID4]
    status: NotificationStatusEnum
    created_at: datetime
    before: datetime
