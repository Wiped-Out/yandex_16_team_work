import asyncio

import aiohttp
import aioredis
import pytest

from typing import Optional
from dataclasses import dataclass
from multidict import CIMultiDictProxy
from elasticsearch import AsyncElasticsearch
import json
from .settings import settings


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
async def es_client():
    es = AsyncElasticsearch(
        hosts=[f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}']
    )

    yield es
    await es.close()


@pytest.fixture(scope='session')
async def redis_client():
    redis = await aioredis.create_redis_pool((
        settings.REDIS_HOST, settings.REDIS_PORT
    ), minsize=10, maxsize=20)

    yield redis

    redis.close()
    await redis.wait_closed()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def create_index(es_client: AsyncElasticsearch):
    async def inner(index: str):
        with open(settings.INDEXES_NAMES_MAPPINGS[index]) as index_mapping_file:
            loaded_json = json.load(index_mapping_file)
            await es_client.indices.create(index=index, body=loaded_json)

    return inner


@pytest.fixture
def load_data(es_client: AsyncElasticsearch):
    async def inner(index: str, filename: str):
        with open(f"../testdata/prepared_data/{filename}") as data:
            loaded_json = json.load(data)
            items = loaded_json['items']
            items_for_bulk = []
            for item in items:
                items_for_bulk += \
                    [
                        {'index': {
                            '_index': index,
                            '_id': item['id']
                        }
                        },

                        item
                    ]

            await es_client.bulk(index=index, body=items_for_bulk)

    return inner


@pytest.fixture
def flush_redis(redis_client: aioredis.Redis):
    async def inner():
        await redis_client.flushall()

    return inner


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
def delete_data(es_client: AsyncElasticsearch):
    async def inner(index: str):
        await es_client.indices.delete(index=index)

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
