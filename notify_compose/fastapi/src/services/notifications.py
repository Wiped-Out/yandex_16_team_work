from functools import lru_cache
from typing import Optional

from db.db import get_db
from models.models import AddNotification, Notification
from pydantic import UUID4
from services.main_db import AbstractMainStorage, MainStorage

from fastapi import Depends


class NotificationsService(MainStorage):
    collection: str = 'notifications'

    async def add_notification(self, notification: AddNotification):
        return await self.create(
            collection=self.collection,
            item=Notification(**notification.dict())
        )

    async def get_notifications(self) -> list[Notification]:
        items: list[dict] = await self.get_all(collection=self.collection)
        return [Notification(**item) for item in items]

    async def get_notification(self, notification_id: UUID4) -> Optional[Notification]:
        item = await self.get_one(collection=self.collection, uuid=notification_id)
        if not item:
            return None
        return Notification(**item)

    async def delete_notification(self, notification_id: UUID4):
        await self.delete(collection=self.collection, uuid=notification_id)


@lru_cache()
def get_notifications_service(
        db: AbstractMainStorage = Depends(get_db),
) -> NotificationsService:
    return NotificationsService(db=db)
