from dataclasses import dataclass
from typing import Optional

import psycopg2
from backoff import backoff
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor


@dataclass
class PostgreSQLManager:
    """Контекстный менеджер для работы с PostgreSQL"""
    dsl: dict
    connection: Optional[_connection] = None

    def __post_init__(self):
        self.connect()

    @backoff()
    def connect(self):
        self.connection = psycopg2.connect(**self.dsl,
                                           cursor_factory=DictCursor)

    def __enter__(self) -> _connection:
        return self.connection

    def __exit__(self, error: Exception, value: object, traceback: object):
        self.connection.commit()
        self.connection.close()
