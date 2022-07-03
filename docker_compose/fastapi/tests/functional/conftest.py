import asyncio

import aiohttp
import pytest

from typing import Optional
from dataclasses import dataclass
from multidict import CIMultiDictProxy
from .settings import settings

pytest_plugins = [
    "fixtures.elastic",
    "fixtures.redis",
]


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        url = f'{settings.API_URL}/api/v1{method}'
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def prepare_for_test(
        create_index,
        load_data,
        flush_redis
):
    async def inner(index: str, filename: str):
        await create_index(index=index)
        await load_data(index=index, filename=filename)
        await asyncio.sleep(1)
        await flush_redis()

    return inner
