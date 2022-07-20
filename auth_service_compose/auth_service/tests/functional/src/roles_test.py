import pytest
import json
import aioredis
from http import HTTPStatus
from psycopg2.extensions import connection as _connection


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_json_path, table_name, filename, http_method",
    (
            (
                    "testdata/responses/get_roles.json",
                    "roles",
                    "roles.json",
                    "GET"
            ),
    )
)
async def test_get_roles(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        get_access_token_headers,
        prepare_for_test,
        make_request,
        delete_table,

        response_json_path: str,
        table_name: str,
        filename: str,
        http_method: str
):
    headers = await get_access_token_headers()

    await prepare_for_test(table_name=table_name, filename=filename)

    # Выполнение запроса
    response = await make_request(
        method='/roles',
        http_method=http_method,
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
                    {"name": "Bog", "level": 1000},
                    "roles",
                    "roles.json",
                    "POST"
            ),
    )
)
async def test_create_roles(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        get_access_token_headers,
        prepare_for_test,
        make_request,
        delete_table,

        json_data: dict,
        table_name: str,
        filename: str,
        http_method: str

):
    headers = await get_access_token_headers()

    await prepare_for_test(table_name=table_name, filename=filename)

    # Выполнение запроса
    response = await make_request(
        method='/roles',
        http_method=http_method,
        json=json_data,
        headers=headers,
    )

    # Проверка результата
    assert response.status == HTTPStatus.CREATED

    assert response.body["level"] == int(json_data["level"]) and response.body["name"] == json_data["name"]

    await delete_table(table_name=table_name)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "role_id, response_json_path, table_name, filename, http_method",
    (
            (
                    "2a7c7470-f837-4499-8e99-34c9de3dc0b7",
                    "testdata/responses/get_role.json",
                    "roles",
                    "roles.json",
                    "GET"
            ),
    )
)
async def test_get_role(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        get_access_token_headers,
        prepare_for_test,
        make_request,
        delete_table,

        role_id: str,
        response_json_path: str,
        table_name: str,
        filename: str,
        http_method: str
):
    headers = await get_access_token_headers()

    await prepare_for_test(table_name=table_name, filename=filename)

    # Выполнение запроса
    response = await make_request(
        method=f'/roles/{role_id}',
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
