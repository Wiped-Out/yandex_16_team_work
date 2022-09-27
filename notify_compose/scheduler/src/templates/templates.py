from datetime import datetime, timedelta
from enum import Enum

from core.config import settings
from pydantic import UUID4, BaseModel, Field


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
    user_ids: list
    notification_type: NotificationTypeEnum
    status: NotificationStatusEnum
    before: datetime

    async def get_external_data(self, **kwargs) -> None:
        pass


class ProlongSubscriptionNotificationTemplate(BaseNotificationTemplate):
    template_id: UUID4 = settings.PROLONG_SUBSCRIPTION_TEMPLATE_UUID
    priority: int = 10
    user_ids: list = Field(default_factory=list)
    notification_type: NotificationTypeEnum = NotificationTypeEnum.email
    status: NotificationStatusEnum = NotificationStatusEnum.created
    before: datetime = Field(default_factory=datetime.utcnow)

    def __post_init__(self):
        self.before = datetime.utcnow() + timedelta(minutes=10)

    async def get_external_data(self, **kwargs) -> None:
        self.user_ids.extend(kwargs['user_ids'])


templates = {
    TemplateNamesEnum.prolong_subscription: ProlongSubscriptionNotificationTemplate
}
