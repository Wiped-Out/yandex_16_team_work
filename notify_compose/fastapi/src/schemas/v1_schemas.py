from pydantic import BaseModel
from datetime import datetime
from pydantic.types import UUID4


class TemplateFieldItem(BaseModel):
    name: str
    url: str
    body: dict
    headers: dict
    fetch_pattern: str


class Template(BaseModel):
    id: UUID4
    body: str
    template_type: str
    fields: list[TemplateFieldItem]


class Notification(BaseModel):
    id: UUID4
    template_id: UUID4
    priority: int
    notification_type: int
    user_ids: list[UUID4]
    status: str
    created_at: datetime
    before: datetime
