from functools import lru_cache

from db.queue import get_queue
from fastapi import Depends
from models.models import AddNotification
from services.queue import AbstractQueue, BaseQueue


class QueueService(BaseQueue):
    async def publish_to_queue(self, notification_id: str, notification: AddNotification):
        for user_id in notification.user_ids:
            message = {
                'notification_id': str(notification_id),
                'user_id': str(user_id)
            }
            await self.publish(
                queue_name=notification.notification_type.value,
                message=message,
                priority=notification.priority
            )


@lru_cache()
def get_queue_service(
        queue: AbstractQueue = Depends(get_queue),
) -> QueueService:
    return QueueService(queue=queue)
