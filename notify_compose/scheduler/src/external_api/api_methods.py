from aiohttp import ClientSession
from core.config import settings
from datetime import datetime


async def add_notification() -> int:
    priority = 2

    async with ClientSession() as client:
        async with client.post(
                url=settings.NOTIFY_API_ENDPOINT,
                data={'template_id': settings.TEMPLATE_UUID,
                      'priority': priority,
                      'notification_type': 'email',
                      'user_ids': settings.USER_IDS,
                      'status': 'created',
                      'before': datetime.now()}
        ) as response:
            return response.status
