from pydantic import BaseModel, UUID4
from enum import Enum


class NotificationTypeEnum(str, Enum):
    email = 'email'


class NotificationStatusEnum(str, Enum):
    created = 'created'
    in_progress = 'in_progress'
    failed = 'failed'
    finished = 'finished'


class TemplateNamesEnum(str, Enum):
    prolong_subscription = 'prolong_subscription'


class NotificationTemplate(BaseModel):
    template_id: UUID4
    priority: int
    notification_type: NotificationTypeEnum
    status: NotificationStatusEnum


templates = {
    TemplateNamesEnum.prolong_subscription: NotificationTemplate(
        template_id='4e08df28-32b4-4955-9f22-8b39a609f4d8',
        priority=10,
        notification_type=NotificationTypeEnum.email,
        status=NotificationStatusEnum.created,
    )
}
