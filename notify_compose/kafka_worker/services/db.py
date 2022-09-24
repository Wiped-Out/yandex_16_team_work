from abc import ABC, abstractmethod

from kafka import KafkaConsumer, KafkaProducer


class AbstractMainProducer(ABC):
    @abstractmethod
    async def send(self, topic: str, value: bytes, key: bytes):
        pass


class AbstractMainConsumer(ABC):
    @abstractmethod
    async def subscribe(self, topics: list):
        pass  # noqa: WPS420

    @abstractmethod
    async def consume(self):
        pass  # noqa: WPS420

    @abstractmethod
    async def close(self):
        pass  # noqa: WPS420


class AbstractStorage(AbstractMainProducer, AbstractMainConsumer):
    pass


class BaseKafkaStorage(AbstractStorage):
    def __init__(self, db_producer: KafkaProducer,
                 db_consumer: KafkaConsumer):
        self.db_producer = db_producer
        self.db_consumer = db_consumer

    async def send(self, topic: str, value: bytes, key: bytes):
        self.db_producer.send(topic=topic, value=value, key=key)

    async def subscribe(self, topics: list):
        self.db_consumer.subscribe(topics)

    async def consume(self):
        return self.db_consumer

    async def close(self):
        self.db_consumer.close()


class MainStorage:
    def __init__(self, db: BaseKafkaStorage):
        self.db = db

    async def send(self, topic: str, value: bytes, key: bytes):
        return await self.db.send(topic=topic, value=value, key=key)

    async def subscribe(self, topics: list):
        return await self.db.subscribe(topics=topics)

    async def consume(self):
        return await self.db.consume()

    async def close(self):
        return await self.db.close()
