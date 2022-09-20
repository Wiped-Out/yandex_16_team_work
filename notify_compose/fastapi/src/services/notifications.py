from functools import lru_cache


class NotificationsService:
    pass


@lru_cache()
def get_notifications_service() -> NotificationsService:
    return NotificationsService()
