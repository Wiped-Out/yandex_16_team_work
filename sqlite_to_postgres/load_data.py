import os
import sqlite3
from contextlib import contextmanager

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from postgres_saver import PostgresSaver
from sqlite_loader import SQLiteLoader

# Для выгрузки/загрузки данных по n записей
PG_PAGE_SIZE = 500
SQLITE_PAGE_SIZE = 500


@contextmanager
def pg_manager(pg_conn: _connection):
    try:
        yield pg_conn
    finally:
        pg_conn.commit()
        pg_conn.close()


class SQLiteManager:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.connection = sqlite3.connect(self.file_name)

    def __enter__(self):
        return self.connection

    def __exit__(self, error: Exception, value: object, traceback: object):
        self.connection.commit()
        self.connection.close()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    # Инициализируем классы для выгрузки и сохранения
    postgres_saver = PostgresSaver(pg_conn, PG_PAGE_SIZE)
    sqlite_loader = SQLiteLoader(connection, SQLITE_PAGE_SIZE)

    # Кортеж таблиц для выгрузки/загрузки
    tables = ('filmworks',
              'genres',
              'persons',
              'genres_filmworks',
              'persons_filmworks')

    # Выгружаем данные из SQLite и сохраняем в PostgreSQL
    for table in tables:
        get_from_sqlite_func = getattr(sqlite_loader,
                                       'get_{table}'.format(table=table))
        load_to_postgres_func = getattr(postgres_saver,
                                        'save_{table}'.format(table=table))
        flow_of_data = get_from_sqlite_func()
        for data in flow_of_data:
            load_to_postgres_func(data)


if __name__ == '__main__':
    psycopg2.extras.register_uuid()
    load_dotenv()
    dsl = {'dbname': os.environ.get('DB_NAME'),
           'user': os.environ.get('DB_USER'),
           'password': os.environ.get('DB_PASSWORD'),
           'host': os.environ.get('DB_HOST', '127.0.0.1'),
           'port': os.environ.get('DB_PORT', 5434)}
    with SQLiteManager('db.sqlite') as sqlite_conn, \
            pg_manager(psycopg2.connect(**dsl,
                                        cursor_factory=DictCursor)) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
