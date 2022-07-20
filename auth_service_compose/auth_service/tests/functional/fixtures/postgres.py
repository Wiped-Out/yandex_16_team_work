import json
import sys
from dataclasses import dataclass, astuple

import psycopg2
import pytest
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from psycopg2.extras import execute_batch
from pydantic import BaseSettings
from pydantic import validate_arguments

sys.path.append("..")

from settings import settings

PG_PAGE_SIZE = 500


class PostgresDSL(BaseSettings):
    dbname: str = settings.POSTGRES_DB_NAME
    user: str = settings.POSTGRES_USER
    password: str = settings.POSTGRES_PASSWORD
    host: str = settings.POSTGRES_HOST
    port: int = settings.POSTGRES_PORT


# Наследуемый класс для базовых функций
@dataclass
class BaseDataclass:
    # Для реализации распаковки
    def __iter__(self):
        return iter(astuple(self))


@validate_arguments
@dataclass
class User(BaseDataclass):
    id: str
    login: str
    email: str
    password: str


@validate_arguments
@dataclass
class Role(BaseDataclass):
    id: str
    name: str
    level: int


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
            unpacked_users = tuple(tuple(i) for i in users)
            execute_batch(
                cur,
                sql_query,
                unpacked_users,
                page_size=self.page_size
            )
        self.pgconn.commit()

    def save_roles(self, roles: list[Role]):
        with self.pgconn.cursor() as cur:
            sql_query = """
            INSERT INTO content.roles
            (id, name, level)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
            """
            unpacked_roles = tuple(tuple(i) for i in roles)
            execute_batch(
                cur,
                sql_query,
                unpacked_roles,
                page_size=self.page_size
            )
        self.pgconn.commit()


@pytest.fixture(scope='session')
async def postgres_connection():
    dsl = PostgresDSL().dict()
    dsl["user"] = "app"
    async with PostgresManager(**dsl, cursor_factory=DictCursor) as pg_conn:
        yield pg_conn


class PostgresManager:
    """Контекстный менеджер для работы с Postgres"""

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    async def connect(self):
        self.connection = psycopg2.connect(**self.kwargs)

    async def __aenter__(self) -> _connection:
        await self.connect()
        return self.connection

    async def __aexit__(self, error: Exception, value: object, traceback: object):
        self.connection.commit()
        self.connection.close()


@pytest.fixture
def create_table(postgres_connection: _connection):
    async def inner(table_name: str):
        with open(settings.TABLES_NAMES_MAPPINGS[table_name], "rt") as file:
            with postgres_connection.cursor() as cursor:
                cursor.execute(file.read())

    return inner


@pytest.fixture
def load_data(postgres_connection: _connection):
    async def inner(table_name: str, path: str):
        postgres_saver = PostgresSaver(postgres_connection, PG_PAGE_SIZE)
        if table_name == "users":
            with open(path, "rt") as file:
                users: list[User] = [User(**user) for user in json.loads(file.read())["items"]]
            print("Сохранил данные в базу данных")
            postgres_saver.save_users(users)
        elif table_name == "roles":
            with open(path, "rt") as file:
                roles: list[Role] = [Role(**role) for role in json.loads(file.read())["items"]]
            print("Сохранил данные в базу данных")
            postgres_saver.save_roles(roles)
        elif table_name == "user_roles":
            # todo
            pass
        else:
            raise ValueError("Incorrect table name")

    return inner


@pytest.fixture
def delete_table(postgres_connection: _connection):
    async def inner(table_name: str):
        schema = "content"
        with postgres_connection.cursor() as cursor:
            cursor.execute(f"DROP TABLE {schema}.{table_name} CASCADE;")

    return inner
