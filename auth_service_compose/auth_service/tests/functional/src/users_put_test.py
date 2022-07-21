import pytest
import aioredis
from http import HTTPStatus
from psycopg2.extensions import connection as _connection

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "user_id, json, http_method",
    (
            (
                    "ed5b50a1-2f79-43e9-918d-87140bb9afd9",
                    {"password": "hirnim-fogkuj-pUrhi4",
                     "new_password": "NewNewPassword",
                     "new_password_repeat": "NewNewPassword"
                     },
                    "PUT",
            ),
    )
)
async def test_update_user_password(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        get_access_token_headers,
        make_request,
        delete_tables,

        user_id: str,
        json: dict,
        http_method: str
):
    headers = await get_access_token_headers()

    # Выполнение запроса
    response = await make_request(
        method=f'/users/{user_id}',
        http_method=http_method,
        json=json,
        headers=headers,
    )

    # Проверка результата
    assert response.status == HTTPStatus.NO_CONTENT

    await delete_tables()


@pytest.mark.parametrize(
    "user_id, json, http_method",
    (
            (
                    "ed5b50a1-2f79-43e9-918d-87140bb9afd9",
                    {"password": "hirnim-fogkuj-pUrhi4",
                     "login": "test",
                     },
                    "PUT",
            ),
    )
)
async def test_update_user_login(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        get_access_token_headers,
        make_request,
        delete_tables,

        user_id: str,
        json: dict,
        http_method: str,
):
    headers = await get_access_token_headers()

    # Выполнение запроса
    response = await make_request(
        method=f'/users/{user_id}',
        http_method=http_method,
        json=json,
        headers=headers,
    )

    # Проверка результата
    assert response.status == HTTPStatus.NO_CONTENT

    await delete_tables()


@pytest.mark.parametrize(
    "user_id, json, http_method",
    (
            (
                    "ed5b50a1-2f79-43e9-918d-87140bb9afd9",
                    {"password": "hirnim-fogkuj-pUrhi4",
                     "email": "new_email@mail.com"
                     },
                    "PUT",
            ),
    )
)
async def test_update_user_email(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        get_access_token_headers,
        make_request,
        delete_tables,

        user_id: str,
        json: dict,
        http_method: str
):
    headers = await get_access_token_headers()

    # Выполнение запроса
    response = await make_request(
        method=f'/users/{user_id}',
        http_method=http_method,
        json=json,
        headers=headers
    )

    # Проверка результата
    assert response.status == HTTPStatus.NO_CONTENT

    await delete_tables()


@pytest.mark.parametrize(
    "user_id, json, http_method",
    (
            (
                    "ed5b50a1-2f79-43e9-918d-87140bb9afd9",
                    {"password": "hirnim-fogkuj-pUrhi4",
                     "email": "new_email@mail.com",
                     "login": "test",
                     },
                    "PUT",
            ),
    )
)
async def test_update_user_login_and_email(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        get_access_token_headers,
        make_request,
        delete_tables,

        user_id: dict,
        json: dict,
        http_method: str
):
    headers = await get_access_token_headers()

    # Выполнение запроса
    response = await make_request(
        method=f'/users/{user_id}',
        http_method=http_method,
        json=json,
        headers=headers,
    )

    # Проверка результата
    assert response.status == HTTPStatus.NO_CONTENT

    await delete_tables()


@pytest.mark.parametrize(
    "user_id, json, http_method",
    (
            (
                    "ed5b50a1-2f79-43e9-918d-87140bb9afd9",
                    {"password": "hirnim-fogkuj-pUrhi4",
                     "new_password": "NewNewPassword",
                     },
                    "PUT",
            ),
    )
)
async def test_update_password_without_confirmation(
        postgres_connection: _connection,
        redis_client: aioredis.Redis,
        get_access_token_headers,
        make_request,
        delete_tables,

        user_id: str,
        json: dict,
        http_method: str
):
    headers = await get_access_token_headers()

    # Выполнение запроса
    response = await make_request(
        method=f'/users/{user_id}',
        http_method=http_method,
        json=json,
        headers=headers
    )

    # Проверка результата
    assert response.status == HTTPStatus.BAD_REQUEST

    await delete_tables()
