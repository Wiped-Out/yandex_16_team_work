from datetime import datetime
from enum import Enum

from pydantic import Field, UUID4, validator

from models.base import BaseOrjsonModel


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
