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


@validate_arguments
@dataclass
class UserRole(BaseDataclass):
    user_id: str
    role_id: str


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

    def save_user_roles(self, user_roles: list[UserRole]):
        with self.pgconn.cursor() as cur:
            sql_query = """
            INSERT INTO content.user_roles
            (user_id, role_id)
            VALUES (%s, %s)
            ON CONFLICT (id) DO NOTHING;
            """
            unpacked_user_roles = tuple(tuple(i) for i in user_roles)
            execute_batch(
                cur,
                sql_query,
                unpacked_user_roles,
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
def prepare_tables(prepare_for_test):
    async def inner():
        table_to_file = {"roles": "roles.json", "users": "users.json", "user_roles": "user_roles.json"}
        for key, value in table_to_file:
            await prepare_for_test(table_name=key, filename=value)

        return inner


@pytest.fixture
def create_table(postgres_connection: _connection):
    async def inner(table_name: str):
        with open(settings.TABLES_NAMES_MAPPINGS[table_name], "rt") as file:
            with postgres_connection.cursor() as cursor:
                cursor.execute(file.read())

                postgres_connection.commit()

    return inner


@pytest.fixture
def load_data(postgres_connection: _connection):
    async def inner(table_name: str, path: str):
        postgres_saver = PostgresSaver(postgres_connection, PG_PAGE_SIZE)
        model, func = {"users": {"model": User, "function": postgres_saver.save_users},
                       "roles": {"model": Role, "function": postgres_saver.save_roles},
                       "user_roles": {"model": UserRole, "function": postgres_saver.save_user_roles}
                       }[table_name]

        with open(path, "rt") as file:
            items = [model(**item) for item in json.loads(file.read())["items"]]
        func(items)

    return inner


@pytest.fixture
def delete_tables(postgres_connection: _connection):
    async def inner():
        schema = "content"
        tables = ["user_roles", "roles", "users"]
        for table in tables:
            with postgres_connection.cursor() as cursor:
                cursor.execute(f"DROP TABLE {schema}.{table} CASCADE;")
                postgres_connection.commit()

    return inner
