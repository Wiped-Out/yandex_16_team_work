import pytest
import json
import aioredis
from http import HTTPStatus
from psycopg2.extensions import connection as _connection


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params, response_json_path, table_name, filename, http_method",
    (
            (
                    {},
                    "testdata/responses/get_users.json",
                    "users",
                    "users.json",
                    "GET"
            ),
    )
)
async def test_get_users(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        get_access_token_headers,
        make_request,
        delete_table,

        params: dict,
        response_json_path: str,
        table_name: str,
        filename: str,
        http_method: str
):
    headers = await get_access_token_headers()

    # Выполнение запроса
    response = await make_request(
        method='/users',
        http_method=http_method,
        params=params,
        headers=headers
    )

    # Проверка результата
    assert response.status == HTTPStatus.OK

    with open(response_json_path) as expected_response:
        expected = json.load(expected_response)["items"]
        assert response.body == expected

    await delete_table(table_name=table_name)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "json_data, table_name, filename, http_method",
    (
            (
                    {"email": "some_email1@example.com", "login": "user1", "password": "user"},
                    "users",
                    "users.json",
                    "POST"
            ),
    )
)
async def test_create_user(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        get_access_token_headers,
        make_request,
        delete_table,

        json_data: dict,
        table_name: str,
        filename: str,
        http_method: str

):
    headers = await get_access_token_headers()

    # Выполнение запроса
    response = await make_request(
        method='/users',
        http_method=http_method,
        json=json_data,
        headers=headers,
    )

    # Проверка результата
    assert response.status == HTTPStatus.CREATED

    assert response.body["email"] == json_data["email"] and response.body["login"] == json_data["login"]

    await delete_table(table_name=table_name)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_id, response_json_path, table_name, filename, http_method",
    (
            (
                    "34b94f10-35da-4918-a199-985af3c8160b",
                    "testdata/responses/get_user.json",
                    "users",
                    "users.json",
                    "GET"
            ),
    )
)
async def test_get_user(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        get_access_token_headers,
        make_request,
        delete_table,

        user_id: str,
        response_json_path: str,
        table_name: str,
        filename: str,
        http_method: str
):
    headers = await get_access_token_headers()

    # Выполнение запроса
    response = await make_request(
        method=f'/users/{user_id}',
        http_method=http_method,
        params={},
        headers=headers,
    )

    # Проверка результата
    assert response.status == HTTPStatus.OK

    with open(response_json_path) as expected_response:
        expected = json.load(expected_response)
        assert response.body == expected

    await delete_table(table_name=table_name)
