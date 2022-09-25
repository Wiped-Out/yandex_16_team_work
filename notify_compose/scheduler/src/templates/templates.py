from pydantic import BaseModel, UUID4, Field
from enum import Enum
from datetime import datetime, timedelta


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
    priority: int = 10
    notification_type: NotificationTypeEnum = NotificationTypeEnum.email
    status: NotificationStatusEnum = NotificationStatusEnum.created
    before: datetime = Field(default_factory=datetime.utcnow)

    def __post_init__(self):
        self.before = datetime.utcnow() + timedelta(minutes=10)


templates = {
    TemplateNamesEnum.prolong_subscription: NotificationTemplate
}
