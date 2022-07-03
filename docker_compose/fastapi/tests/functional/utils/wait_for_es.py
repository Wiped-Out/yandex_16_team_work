from elasticsearch import AsyncElasticsearch

from settings import settings
from .utils import backoff_on_true, backoff


class ElasticManager:
    """Контекстный менеджер для работы с Elasticsearch"""

    @backoff()
    async def connect(self):
        self.connection = AsyncElasticsearch(
            hosts=[f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}']
        )

    async def __aenter__(self) -> AsyncElasticsearch:
        await self.connect()
        return self.connection

    async def __aexit__(self, error: Exception, value: object, traceback: object):
        await self.connection.close()


@backoff_on_true()
async def wait_for_es():
    async with ElasticManager() as es:
        return await es.ping()
