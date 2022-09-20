from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from pydantic.types import UUID4
from datetime import datetime
from services.notifications import NotificationsService, get_notifications_service
from schemas.v1_schemas import Notification

router = APIRouter()


class AddNotification(BaseModel):
    id: UUID4
    template_id: UUID4
    priority: int
    type: int
    user_ids: list[UUID4]
    status: str
    created_at: datetime
    before: datetime


@router.post(
    path='',
    description='Add notification'
)
async def add_notification(
        notification: AddNotification,
        notifications_service: NotificationsService = Depends(get_notifications_service),
):
    # todo
    pass


@router.get(
    path='',
    description='Get notifications',
    response_model=list[Notification],
)
async def get_notifications(
        notifications_service: NotificationsService = Depends(get_notifications_service),
):
    # todo
    pass


@router.get(
    path='/{notification_id}',
    description='Get notification by id',
    response_model=Optional[Notification],
)
async def get_notification(
        notification_id: str,
        notifications_service: NotificationsService = Depends(get_notifications_service),
):
    # todo
    pass


@router.delete(
    path='/{notification_id}',
    description='Delete notification',
)
async def delete_notification(
        notification_id: str,
        notifications_service: NotificationsService = Depends(get_notifications_service),
):
    # todo
    pass
