from abc import ABC, abstractmethod

from extensions.tracer import _trace
from kafka import KafkaProducer


class AbstractProducer(ABC):
    @abstractmethod
    def send(self, topic: str, value: bytes, key: bytes):
        pass


class BaseKafkaProducer(AbstractProducer):
    def __init__(self, db_producer: KafkaProducer):
        self.db_producer = db_producer

    def send(self, topic: str, value: bytes, key: bytes):
        self.db_producer.send(topic=topic, value=value, key=key)


class MainProducer:
    def __init__(self, db: BaseKafkaProducer):
        self.db = db

    @_trace()
    def send(self, topic: str, value: bytes, key: bytes):
        return self.db.send(topic=topic, value=value, key=key)
