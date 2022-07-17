import pytest
import json
import aioredis
from http import HTTPStatus
from psycopg2.extensions import connection as _connection


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params, response_json_path, table_name, filename, request_method",
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
        prepare_for_test,
        make_get_request,
        delete_table,

        params: dict,
        response_json_path: str,
        table_name: str,
        filename: str,
        request_method: str
):
    await prepare_for_test(table_name=table_name, filename=filename)

    # Выполнение запроса
    response = await make_get_request(
        method='/users',
        request_method=request_method,
        params=params
    )

    # Проверка результата
    assert response.status == HTTPStatus.OK

    with open(response_json_path) as expected_response:
        expected = json.load(expected_response)
        assert response.body == expected

    await delete_table(table_name=table_name)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params, table_name, filename, request_method",
    (
            (
                    {"email": "some_email@example.com", "login": "user", "password": "user"},
                    "users",
                    "users.json"
                    "POST"
            ),
    )
)
async def test_create_user(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        prepare_for_test,
        make_get_request,
        delete_table,

        params: dict,
        table_name: str,
        filename: str,
        request_method: str

):
    await prepare_for_test(table_name=table_name, filename=filename)

    # Выполнение запроса
    response = await make_get_request(
        method='/users',
        request_method=request_method,
        params=params
    )

    # Проверка результата
    assert response.status == HTTPStatus.CREATED

    assert response.body["email"] == params["email"] and response.body["login"] == params["login"]

    await delete_table(table_name=table_name)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_id, response_json_path, table_name, filename, request_method",
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
        prepare_for_test,
        make_get_request,
        delete_table,

        user_id: dict,
        response_json_path: str,
        table_name: str,
        filename: str,
        request_method: str
):
    await prepare_for_test(table_name=table_name, filename=filename)

    # Выполнение запроса
    response = await make_get_request(
        method=f'/users/{user_id}',
        request_method=request_method,
        params={}
    )

    # Проверка результата
    assert response.status == HTTPStatus.OK

    with open(response_json_path) as expected_response:
        expected = json.load(expected_response)
        assert response.body == expected

    await delete_table(table_name=table_name)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_id, response_json_path, table_name, filename, request_method",
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
async def test_update_user_password(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        prepare_for_test,
        make_get_request,
        delete_table,

        user_id: dict,
        response_json_path: str,
        table_name: str,
        filename: str,
        request_method: str
):
    # todo
    await prepare_for_test(table_name=table_name, filename=filename)

    # Выполнение запроса
    response = await make_get_request(
        method=f'/users/{user_id}',
        request_method=request_method,
        params={}
    )

    # Проверка результата
    assert response.status == HTTPStatus.OK

    with open(response_json_path) as expected_response:
        expected = json.load(expected_response)
        assert response.body == expected

    await delete_table(table_name=table_name)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_id, response_json_path, table_name, filename, request_method",
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
async def test_update_user_login(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        prepare_for_test,
        make_get_request,
        delete_table,

        user_id: dict,
        response_json_path: str,
        table_name: str,
        filename: str,
        request_method: str
):
    # todo
    await prepare_for_test(table_name=table_name, filename=filename)

    # Выполнение запроса
    response = await make_get_request(
        method=f'/users/{user_id}',
        request_method=request_method,
        params={}
    )

    # Проверка результата
    assert response.status == HTTPStatus.OK

    with open(response_json_path) as expected_response:
        expected = json.load(expected_response)
        assert response.body == expected

    await delete_table(table_name=table_name)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_id, response_json_path, table_name, filename, request_method",
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
async def test_update_user_email(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        prepare_for_test,
        make_get_request,
        delete_table,

        user_id: dict,
        response_json_path: str,
        table_name: str,
        filename: str,
        request_method: str
):
    # todo
    await prepare_for_test(table_name=table_name, filename=filename)

    # Выполнение запроса
    response = await make_get_request(
        method=f'/users/{user_id}',
        request_method=request_method,
        params={}
    )

    # Проверка результата
    assert response.status == HTTPStatus.OK

    with open(response_json_path) as expected_response:
        expected = json.load(expected_response)
        assert response.body == expected

    await delete_table(table_name=table_name)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_id, response_json_path, table_name, filename, request_method",
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
async def test_update_user_login_and_password(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        prepare_for_test,
        make_get_request,
        delete_table,

        user_id: dict,
        response_json_path: str,
        table_name: str,
        filename: str,
        request_method: str
):
    # todo
    await prepare_for_test(table_name=table_name, filename=filename)

    # Выполнение запроса
    response = await make_get_request(
        method=f'/users/{user_id}',
        request_method=request_method,
        params={}
    )

    # Проверка результата
    assert response.status == HTTPStatus.OK

    with open(response_json_path) as expected_response:
        expected = json.load(expected_response)
        assert response.body == expected

    await delete_table(table_name=table_name)



@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_id, response_json_path, table_name, filename, request_method",
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
async def test_update_password_without_confirmation(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        prepare_for_test,
        make_get_request,
        delete_table,

        user_id: dict,
        response_json_path: str,
        table_name: str,
        filename: str,
        request_method: str
):
    # todo
    await prepare_for_test(table_name=table_name, filename=filename)

    # Выполнение запроса
    response = await make_get_request(
        method=f'/users/{user_id}',
        request_method=request_method,
        params={}
    )

    # Проверка результата
    assert response.status == HTTPStatus.OK

    with open(response_json_path) as expected_response:
        expected = json.load(expected_response)
        assert response.body == expected

    await delete_table(table_name=table_name)

