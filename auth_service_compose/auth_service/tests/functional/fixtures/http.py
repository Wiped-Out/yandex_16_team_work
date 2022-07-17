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
def make_get_request(session):
    async def inner(
            method: str,
            request_method: str,
            params: Optional[dict] = None,
    ) -> HTTPResponse:
        params = params or {}
        url = f'{settings.API_URL}/api/v1{method}'

        func = builtins.getattr(session, request_method.lower())

        async with func(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
