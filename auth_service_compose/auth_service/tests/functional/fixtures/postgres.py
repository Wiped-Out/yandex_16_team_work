import sys
import pytest
import psycopg2
import os
from psycopg2.extras import DictCursor
from pydantic import BaseSettings
from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch
from pydantic import validate_arguments
import uuid
from dataclasses import dataclass, astuple
import json

sys.path.append("..")

from settings import settings

PG_PAGE_SIZE = 500


class PostgresDSL(BaseSettings):
    dbname: str = os.environ.get('DB_NAME')
    user: str = "app"
    password: str = os.environ.get('DB_PASSWORD')
    host: str = os.environ.get('DB_HOST', '127.0.0.1')
    port: int = os.environ.get('DB_PORT', 5434)


# Наследуемый класс для базовых функций
@dataclass
class BaseDataclass:
    # Для реализации распаковки
    def __iter__(self):
        return iter(astuple(self))


@validate_arguments
@dataclass
class User(BaseDataclass):
    id: uuid.UUID
    login: str
    email: str
    password: str


@dataclass
class PostgresSaver:
    """Класс для загрузки данных в PostgreSQL"""
    pgconn: _connection
    page_size: int = 500

    def save_users(self, users: list[User]):
        with self.pgconn.cursor() as cur:
            sql_query = """
            INSERT INTO content.users
            (id, login, email, password)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
            """
            unpacked_filmworks = tuple(tuple(i) for i in users)
            execute_batch(
                cur,
                sql_query,
                unpacked_filmworks,
                page_size=self.page_size
            )


@pytest.fixture(scope='session')
async def postgres_connection():
    dsl = PostgresDSL().dict()
    dsl["user"] = "app"
    with pg_manager(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn:
        yield pg_conn


def pg_manager(pg_conn: _connection):
    try:
        yield pg_conn
    finally:
        pg_conn.commit()
        pg_conn.close()


@pytest.fixture
def create_table(pg_connection: _connection):
    async def inner(index: str):
        with open(settings.TABLES_NAMES_MAPPINGS[index], "rt") as file:
            with pg_connection.cursor() as cursor:
                cursor.execute(file.read())

    return inner


@pytest.fixture
def load_data(pg_connection: _connection):
    async def inner(table_name: str, filename: str):
        postgres_saver = PostgresSaver(pg_connection, PG_PAGE_SIZE)
        if table_name == "users":
            with open(filename, "rt") as file:
                users: list[User] = [User(**user) for user in json.loads(file.read())]
            postgres_saver.save_users(users)
        elif table_name == "roles":
            # todo
            raise ValueError("Incorrect table name")
        else:
            raise ValueError("Incorrect table name")

    return inner


@pytest.fixture
def delete_table(pg_connection: _connection):
    async def inner(table_name: str):
        with pg_connection.cursor() as cursor:
            cursor.execute(f"DROP TABLE {table_name} CASCADE;")

    return inner
