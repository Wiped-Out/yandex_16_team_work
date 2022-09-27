import json
from abc import ABC, abstractmethod
from typing import Any

from aio_pika import DeliveryMode, Message
from aio_pika.abc import AbstractConnection
from core.config import settings
from models.models import NotificationTypeEnum


class AbstractQueue(ABC):
    @abstractmethod
    def publish(self, queue_name: str, message: Any, priority: int):
        pass


class BaseRabbitQueue(AbstractQueue):
    @classmethod
    async def init(cls, connection: AbstractConnection):
        self = BaseRabbitQueue()
        self.connection = connection
        self.channel = await self.connection.channel()
        for item in NotificationTypeEnum:
            await self.channel.declare_queue(
                name=item.value,
                durable=True,
                arguments={'x-max-priority': settings.RABBIT_MAX_PRIORITY}
            )
        return self

    async def publish(self, queue_name: str, message: Any, priority: int) -> None:
        message = Message(
            body=json.dumps(message).encode('utf-8'),
            delivery_mode=DeliveryMode.PERSISTENT,
            priority=priority
        )

        await self.channel.default_exchange.publish(
            message=message,
            routing_key=queue_name,
        )


class BaseQueue:
    def __init__(self, queue: AbstractQueue):
        self.queue = queue

    async def publish(self, queue_name: str, message: Any, priority: int) -> None:
        await self.queue.publish(
            queue_name=queue_name,
            message=message,
            priority=priority
        )
