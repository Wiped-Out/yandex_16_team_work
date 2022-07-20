import builtins
import aiohttp
import pytest

from typing import Optional
from dataclasses import dataclass
from multidict import CIMultiDictProxy
from settings import settings


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def login_user(make_request):
    async def inner() -> str:
        response = await make_request(
            method="/login",
            http_method="POST",
            json={"login": "user",
                  "password": "hirnim-fogkuj-pUrhi4"
                  }
        )

        return response.body.get("access_token")

    return inner


@pytest.fixture
def get_access_token_headers(prepare_for_test, login_user):
    async def inner() -> dict:
        table_to_file = {"roles": "roles.json", "users": "users.json", "user_roles": "user_roles.json"}
        for key, value in table_to_file.items():
            await prepare_for_test(table_name=key, filename=value)

        access_token = await login_user()
        return {"Authorization": f"Bearer {access_token}"}

    return inner


@pytest.fixture
def make_request(session):
    async def inner(
            method: str,
            http_method: str,
            headers: Optional[dict] = None,
            params: Optional[dict] = None,
            json: Optional[dict] = None,
    ) -> HTTPResponse:
        params = params or {}
        headers = headers or {}
        json = json or {}

        url = f'{settings.API_URL}/api/v1{method}'

        func = builtins.getattr(session, http_method.lower())

        async with func(url, params=params, headers=headers, json=json) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
