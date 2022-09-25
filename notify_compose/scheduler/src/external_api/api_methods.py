from aiohttp import ClientSession
from core.config import settings
from templates.templates import NotificationTemplate
from typing import Type


async def add_notification(notification_template: Type[NotificationTemplate]) -> int:
    template = notification_template()

    async with ClientSession() as client:
        async with client.post(
                url=settings.NOTIFY_API_ENDPOINT,
                json={'template_id': template.template_id,
                      'priority': template.priority,
                      'notification_type': template.notification_type,
                      'user_ids': settings.USER_IDS,
                      'status': template.status,
                      'before': template.before}
        ) as response:
            return response.status
