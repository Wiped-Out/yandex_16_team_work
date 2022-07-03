from settings import settings
from elasticsearch import AsyncElasticsearch
from utils.utils import backoff


@backoff()
async def wait_for_es():
    es = AsyncElasticsearch(
        hosts=[f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}']
    )

    await es.close()
