import pytest

from elasticsearch import AsyncElasticsearch
import json
from .settings import settings


@pytest.fixture(scope='session')
async def es_client():
    es = AsyncElasticsearch(
        hosts=[f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}']
    )

    yield es
    await es.close()


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
def delete_data(es_client: AsyncElasticsearch):
    async def inner(index: str):
        await es_client.indices.delete(index=index)

    return inner
