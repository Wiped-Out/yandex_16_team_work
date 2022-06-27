from aioredis import Redis
from elasticsearch import AsyncElasticsearch

from models.film import Film
from models.person import Person
from models.genre import Genre
from elasticsearch import NotFoundError
import json


class BaseRedisService:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.CACHE_EXPIRE_IN_SECONDS = 60 * 5

    async def get_one_item_from_cache(self, cache_key: str, model):
        data = await self.redis.get(key=cache_key)
        if not data:
            return None

        return model.parse_raw(data)

    async def put_one_item_to_cache(self, cache_key: str, item):
        await self.redis.set(
            key=cache_key, value=item.json(),
            expire=self.CACHE_EXPIRE_IN_SECONDS,
        )

    async def get_items_from_cache(self, cache_key: str, model):
        data = await self.redis.get(key=cache_key)
        if not data:
            return []

        return [model.parse_raw(item) for item in json.loads(data)]

    async def put_items_to_cache(self, cache_key: str, items: list):
        await self.redis.set(
            key=cache_key, value=json.dumps([item.json() for item in items]),
            expire=self.CACHE_EXPIRE_IN_SECONDS,
        )


class BaseElasticService:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(
            self, _id: str, model, index: str
    ):
        try:
            doc = await self.elastic.get(index, _id)
        except NotFoundError:
            return None

        return model(**doc["_source"])

    async def get_data_from_elastic(
            self, page: int, page_size: int, model, index: str,
    ):
        query = {
            "query": {
                "match_all": {}
            }
        }

        try:
            doc = await self.elastic.search(
                index=index, body=query,
                from_=page_size * (page - 1),
                size=page_size,
            )
            return [model(**item["_source"]) for item in doc["hits"]["hits"]]
        except NotFoundError:
            return []

    async def count_all_data_in_index(self, index: str) -> int:
        count = await self.elastic.count(index=index)
        return count["count"]

    async def _search_in_elastic(
            self, search: str, fields: list[str], index: str,
            page: int, page_size: int,
    ) -> dict:
        query = {
            "query": {
                "multi_match": {
                    "query": search,
                    "fields": fields,
                    "fuzziness": "auto"
                }
            }
        }

        try:
            doc = await self.elastic.search(
                index=index, body=query,
                from_=page_size * (page - 1),
                size=page_size
            )
        except NotFoundError:
            return {}

        return doc

    async def get_items_by_search(
            self, search: str, fields: list[str], index: str, model,
            page: int, page_size: int,
    ) -> list:
        doc = await self._search_in_elastic(
            search=search, fields=fields, index=index, page=page,
            page_size=page_size,
        )

        if not doc:
            return []

        return [model(**item["_source"]) for item in doc["hits"]["hits"]]


class BaseGenreService(BaseRedisService, BaseElasticService):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        BaseRedisService.__init__(self, redis=redis)
        BaseElasticService.__init__(self, elastic=elastic)

        self.index = "genres"
        self.model = Genre
        self.redis = redis
        self.elastic = elastic


class BaseMovieService(BaseRedisService, BaseElasticService):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        BaseRedisService.__init__(self, redis=redis)
        BaseElasticService.__init__(self, elastic=elastic)

        self.index = "movies"
        self.model = Film
        self.redis = redis
        self.elastic = elastic


class BasePersonService(BaseRedisService, BaseElasticService):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        BaseRedisService.__init__(self, redis=redis)
        BaseElasticService.__init__(self, elastic=elastic)

        self.index = "persons"
        self.model = Person
        self.redis = redis
        self.elastic = elastic
