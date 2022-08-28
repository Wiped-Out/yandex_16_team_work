import os
from contextlib import contextmanager

import psycopg2
from data_faker import DataFaker
from dotenv import load_dotenv
from postgres_saver import PostgresSaver
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from pydantic import BaseSettings

load_dotenv()

# Для генерации/загрузки данных по n записей
PG_PAGE_SIZE = 500
DATA_FAKER_PAGE_SIZE = 500
# Переменные для определения количества фейковых записей
FILMWORKS_AMOUNT = 25_000
GENRES_AMOUNT = 120
PERSONS_AMOUNT = 10_000


class PostgresDSL(BaseSettings):
    dbname: str = os.environ.get('DB_NAME')
    user: str = 'app'
    password: str = os.environ.get('DB_PASSWORD')
    host: str = os.environ.get('DB_HOST', '127.0.0.1')
    port: int = os.environ.get('DB_PORT', 5434)


@contextmanager
def pg_manager(pg_conn: _connection):
    try:
        yield pg_conn
    finally:
        pg_conn.commit()
        pg_conn.close()


def load_fake_data(pg_conn: _connection):
    """Основной метод загрузки данных фейковых данных в Postgres"""
    # Инициализируем классы для создания фейковых данных и сохранения
    postgres_saver = PostgresSaver(pg_conn, PG_PAGE_SIZE)
    data_faker = DataFaker(DATA_FAKER_PAGE_SIZE,
                           FILMWORKS_AMOUNT,
                           GENRES_AMOUNT,
                           PERSONS_AMOUNT)

    # Кортеж таблиц для загрузки
    tables = ('filmworks',
              'genres',
              'persons',
              'genres_filmworks',
              'persons_filmworks')
    # Создаём фейковые данные и сохраняем в PostgreSQL
    for table in tables:
        get_fake_data_func = getattr(data_faker,
                                     'get_{table}'.format(table=table))
        load_to_postgres_func = getattr(postgres_saver,
                                        'save_{table}'.format(table=table))
        flow_of_data = get_fake_data_func()
        for data in flow_of_data:
            load_to_postgres_func(data)


if __name__ == '__main__':
    psycopg2.extras.register_uuid()
    dsl = PostgresDSL().dict()
    dsl['user'] = 'app'
    with pg_manager(psycopg2.connect(**dsl,
                                     cursor_factory=DictCursor)) as pg_conn:
        load_fake_data(pg_conn)
