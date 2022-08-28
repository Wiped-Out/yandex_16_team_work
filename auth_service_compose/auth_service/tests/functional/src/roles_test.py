import json
from http import HTTPStatus

import aioredis
import pytest
from psycopg2.extensions import connection as _connection

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'response_json_path, http_method',
    (
            (
                    'testdata/responses/get_roles.json',
                    'GET',
            ),
    ),
)
async def test_get_roles(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        get_access_token_headers,
        make_request,
        delete_tables,

        response_json_path: str,
        http_method: str,
):
    headers = await get_access_token_headers()

    # Выполнение запроса
    response = await make_request(
        method='/roles',
        http_method=http_method,
        headers=headers,
    )

    # Проверка результата
    assert response.status == HTTPStatus.OK

    with open(response_json_path) as expected_response:
        expected = json.load(expected_response)
        assert response.body['items'] == expected['items']

    await delete_tables()


@pytest.mark.parametrize(
    'json_data, http_method',
    (
            (
                    {'name': 'Bog', 'level': 1000},
                    'POST',
            ),
    ),
)
async def test_create_roles(
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
        method='/roles',
        http_method=http_method,
        json=json_data,
        headers=headers,
    )

    # Проверка результата
    assert response.status == HTTPStatus.CREATED

    is_level_equal = int(response.body['level']) == int(json_data['level'])
    is_name_equal = response.body['name'] == json_data['name']
    assert is_level_equal and is_name_equal

    await delete_tables()


@pytest.mark.parametrize(
    'role_id, response_json_path, http_method',
    (
            (
                    '2a7c7470-f837-4499-8e99-34c9de3dc0b7',
                    'testdata/responses/get_role.json',
                    'GET',
            ),
    ),
)
async def test_get_role(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        get_access_token_headers,
        make_request,
        delete_tables,

        role_id: str,
        response_json_path: str,
        http_method: str,
):
    headers = await get_access_token_headers()

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

    await delete_tables()
