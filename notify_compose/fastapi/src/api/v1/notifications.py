from typing import Optional

from fastapi import APIRouter, Depends
from services.notifications import NotificationsService, get_notifications_service
from schemas.v1_schemas import Notification
from models.models import AddNotification
from pydantic import UUID4

router = APIRouter()


@router.post(
    path='',
    description='Add notification'
)
async def add_notification(
        notification: AddNotification,
        notifications_service: NotificationsService = Depends(get_notifications_service),
):
    await notifications_service.add_notification(notification=notification)
    return {"message": "Notification added"}


@router.get(
    path='',
    description='Get notifications',
    response_model=list[Notification],
)
async def get_notifications(
        notifications_service: NotificationsService = Depends(get_notifications_service),
):
    notifications_db = await notifications_service.get_notifications()
    return [Notification(**notification.dict()) for notification in notifications_db]


@router.get(
    path='/{notification_id}',
    description='Get notification by id',
    response_model=Optional[Notification],
)
async def get_notification(
        notification_id: UUID4,
        notifications_service: NotificationsService = Depends(get_notifications_service),
):
    notification = await notifications_service.get_notification(notification_id=notification_id)
    if not notification:
        return None
    return Notification(**notification.dict())


@router.delete(
    path='/{notification_id}',
    description='Delete notification',
)
async def delete_notification(
        notification_id: UUID4,
        notifications_service: NotificationsService = Depends(get_notifications_service),
):
    await notifications_service.delete_notification(notification_id=notification_id)
    return {"message": "Notification deleted"}
