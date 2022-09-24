from datetime import datetime
from enum import Enum

from models.base import BaseOrjsonModel
from pydantic import UUID4, Field


class NotificationTypeEnum(str, Enum):
    email = 'email'


class NotificationStatusEnum(str, Enum):
    created = 'created'
    in_progress = 'in_progress'
    failed = 'failed'
    finished = 'finished'


class Notification(BaseOrjsonModel):
    template_id: UUID4
    priority: int
    notification_type: NotificationTypeEnum
    user_ids: list[UUID4]
    status: NotificationStatusEnum
    before: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True
