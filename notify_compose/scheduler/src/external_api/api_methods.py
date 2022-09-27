import json
from typing import Type

from aiohttp import ClientSession
from core.config import settings
from templates.templates import BaseNotificationTemplate


async def add_notification(notification_template: Type[BaseNotificationTemplate]) -> int:
    template = notification_template()
    await template.get_external_data(user_ids=settings.USER_IDS)
    async with ClientSession() as client:
        async with client.post(
                url=settings.NOTIFY_API_ENDPOINT,
                json=json.loads(notification_template().json())
        ) as response:
            return response.status
