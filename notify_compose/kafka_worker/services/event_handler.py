import json
from functools import lru_cache
from typing import Type

from core.config import settings
from core.notify_templates import NotificationTemplate
from services.auto_login_requests import AutoLoginRequests


class EventService(AutoLoginRequests):
    def __init__(self,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)

    async def handle_event(self, data_from_topic: bytes, notification_template: Type[NotificationTemplate]):
        item = notification_template()
        await item.handle_data_from_topic(data=json.loads(data_from_topic))
        response = await self.post(url=settings.NOTIFY_API_ENDPOINT, body=json.loads(item.json()))


@lru_cache()
def get_event_service(
):
    return EventService()  # type: ignore
