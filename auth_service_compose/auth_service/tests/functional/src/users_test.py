import pytest
import json
import aioredis
from http import HTTPStatus
from psycopg2.extensions import connection as _connection

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "params, response_json_path, http_method",
    (
            (
                    {},
                    "testdata/responses/get_users.json",
                    "GET",
            ),
    )
)
async def test_get_users(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        get_access_token_headers,
        make_request,
        delete_tables,

        params: dict,
        response_json_path: str,
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
        expected = json.load(expected_response)
        assert response.body["items"] == expected["items"]

    await delete_tables()


@pytest.mark.parametrize(
    "json_data, http_method",
    (
            (
                    {"email": "some_email1@example.com", "login": "user1", "password": "user"},
                    "POST",
            ),
    )
)
async def test_create_user(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        get_access_token_headers,
        make_request,
        delete_tables,

        json_data: dict,
        http_method: str,

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

    await delete_tables()


@pytest.mark.parametrize(
    "user_id, response_json_path, http_method",
    (
            (
                    "34b94f10-35da-4918-a199-985af3c8160b",
                    "testdata/responses/get_user.json",
                    "GET",
            ),
    )
)
async def test_get_user(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        get_access_token_headers,
        make_request,
        delete_tables,

        user_id: str,
        response_json_path: str,
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

    await delete_tables()
