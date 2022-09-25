from aiohttp import ClientSession
from core.config import settings
from uuid import uuid4, UUID
from random import SystemRandom
from datetime import datetime


async def add_notification() -> int:
    priority = 2

    async with ClientSession() as client:
        async with client.post(
                url=settings.NOTIFY_API_ENDPOINT,
                data={'template_id': settings.TEMPLATE_UUID,
                      'priority': priority,
                      'notification_type': 'email',
                      'user_ids': await generate_user_ids(),
                      'status': 'created',
                      'before': datetime.now()}
        ) as response:
            return response.status


async def generate_user_ids() -> list[UUID]:
    # todo позже айди юзеров будут получаться из ручек других сервисов (UGC)
    user_ids = []
    for _ in range(SystemRandom().randint(1, 100)):
        user_ids.append(uuid4())
    return user_ids
