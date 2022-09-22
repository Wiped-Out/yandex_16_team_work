from datetime import datetime, timedelta

from models.models import Notification, NotificationTypeEnum, NotificationStatusEnum
from pydantic import UUID4, Field


class NotificationTemplate(Notification):

    async def handle_data_from_topic(self, data: dict):
        pass


class EmailConfirmationTemplate(NotificationTemplate):
    template_id: UUID4 = 'a87944ff-cf6c-49e6-a7d8-84f89c41c3e8'
    priority: int = 10
    notification_type: NotificationTypeEnum = NotificationTypeEnum.email
    user_ids: list[UUID4] = Field(default_factory=list)
    status: NotificationStatusEnum = NotificationStatusEnum.created
    before: datetime = Field(default_factory=datetime.utcnow)

    def __post_init__(self):
        self.before = datetime.utcnow() + timedelta(minutes=10)

    async def handle_data_from_topic(self, data: dict) -> None:
        self.user_ids.append(data['user_id'])


class PasswordGenerationTemplate(EmailConfirmationTemplate):
    template_id: UUID4 = '3e7f1f76-533b-441c-95a3-a559e53f9ffc'


topics_to_notify_template = {
    'email_confirmation':
        EmailConfirmationTemplate,
    'password_generation': PasswordGenerationTemplate

}
