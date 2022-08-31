from abc import ABC, abstractmethod

from kafka import KafkaProducer


class AbstractMainStorage(ABC):
    @abstractmethod
    def send(self, topic: str, value: bytes, key: bytes):
        pass


class BaseKafkaStorage(AbstractMainStorage):
    def __init__(self, db: KafkaProducer):
        self.db = db

    def send(self, topic: str, value: bytes, key: bytes):
        self.db.send(topic=topic, value=value, key=key)


class MainStorage:
    def __init__(self, db: BaseKafkaStorage):
        self.db = db

    def send(self, topic: str, value: bytes, key: bytes):
        self.db.send(topic=topic, value=value, key=key)
