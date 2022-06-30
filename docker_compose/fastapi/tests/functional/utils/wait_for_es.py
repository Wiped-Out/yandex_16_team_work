from settings import settings
from elasticsearch import AsyncElasticsearch

async def wait_for_es():
    es = AsyncElasticsearch(
        hosts=[f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}']
    )

    while not await es.ping():
        pass

    await es.close()