from aiohttp import ClientSession
from core.config import settings
from datetime import datetime
from templates.templates import NotificationTemplate


async def add_notification(notification_template: NotificationTemplate) -> int:
    async with ClientSession() as client:
        async with client.post(
                url=settings.NOTIFY_API_ENDPOINT,
                data={'template_id': notification_template.template_id,
                      'priority': notification_template.priority,
                      'notification_type': notification_template.notification_type,
                      'user_ids': settings.USER_IDS,
                      'status': notification_template.status,
                      'before': datetime.now()}
        ) as response:
            return response.status
