from dataclasses import dataclass
from typing import Optional

from backoff import backoff
from elasticsearch import Elasticsearch


@dataclass
class ElasticSearchManager:
    """Контекстный менеджер для работы с Elasticsearch"""
    url: str
    connection: Optional[Elasticsearch] = None

    def __post_init__(self):
        self.connect()

    @backoff()
    def connect(self):
        self.connection = Elasticsearch(self.url)

    def __enter__(self) -> Elasticsearch:
        return self.connection

    def __exit__(self, error: Exception, value: object, traceback: object):
        self.connection = None
