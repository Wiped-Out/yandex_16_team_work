from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import UUID4

from models.models import AddNotification
from schemas.v1_schemas import Notification, Created
from services.notifications import NotificationsService, get_notifications_service

router = APIRouter()


@router.post(
    path='',
    description='Add notification',
    response_model=Created,
    status_code=HTTPStatus.CREATED
)
async def add_notification(
        notification: AddNotification,
        notifications_service: NotificationsService = Depends(get_notifications_service),
):
    item_id = await notifications_service.add_notification(notification=notification)
    return Created(id=item_id)


@router.get(
    path='',
    description='Get notifications',
    response_model=list[Notification],
    status_code=HTTPStatus.OK
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
    status_code=HTTPStatus.OK
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
    status_code=HTTPStatus.NO_CONTENT
)
async def delete_notification(
        notification_id: UUID4,
        notifications_service: NotificationsService = Depends(get_notifications_service),
):
    await notifications_service.delete_notification(notification_id=notification_id)
