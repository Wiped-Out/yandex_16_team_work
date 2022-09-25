from pydantic import BaseModel, UUID4
from enum import Enum
from datetime import datetime, timedelta
from core.config import settings


class NotificationTypeEnum(str, Enum):
    email = 'email'


class NotificationStatusEnum(str, Enum):
    created = 'created'
    in_progress = 'in_progress'
    failed = 'failed'
    finished = 'finished'


class TemplateNamesEnum(str, Enum):
    prolong_subscription = 'prolong_subscription'


class BaseNotificationTemplate(BaseModel):
    template_id: UUID4
    priority: int
    notification_type: NotificationTypeEnum
    status: NotificationStatusEnum
    before: datetime


class ProlongSubscriptionNotificationTemplate(BaseNotificationTemplate):
    template_id: UUID4 = settings.PROLONG_SUBSCRIPTION_TEMPLATE_UUID
    priority: int = 10
    notification_type: NotificationTypeEnum = NotificationTypeEnum.email
    status: NotificationStatusEnum = NotificationStatusEnum.created

    def __post_init__(self):
        self.before = datetime.utcnow() + timedelta(minutes=10)


templates = {
    TemplateNamesEnum.prolong_subscription: ProlongSubscriptionNotificationTemplate
}
