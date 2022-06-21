from aioredis import Redis
from elasticsearch import AsyncElasticsearch

from models.film import Film
from models.person import Person, PersonType
from models.genre import Genre
from typing import Optional
from elasticsearch import NotFoundError


class BaseService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.CACHE_EXPIRE_IN_SECONDS = 60 * 5

    async def _get_from_elastic_by_id(
            self, _id: str, model, index: str
    ):
        try:
            doc = await self.elastic.get(index, _id)
        except NotFoundError:
            return None

        return model(**doc["_source"])

    async def _get_from_elastic_by_search(
            self, search: str, fields: list[str], index: str, model,
            page: int, page_size: int,
    ):
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
            return [model(**item["_source"]) for item in doc["hits"]["hits"]]
        except NotFoundError:
            return []

    async def _get_all_data_from_elastic(
            self, index: str, model, page: int, page_size: int
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


class BaseGenreService(BaseService):
    model = Genre

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        super().__init__(redis, elastic)
        self.index = "genres"

    async def _put_genre_to_cache(self, genre: Genre, cache_key: str):
        await self.redis.set(
            key=cache_key, value=genre.json(),
            expire=self.CACHE_EXPIRE_IN_SECONDS,
        )


class BaseMovieService(BaseService):
    model = Film

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        super().__init__(redis, elastic)
        self.index = "movies"

    async def _search_films_in_elastic(
            self, search: str, page_size: int, page: int
    ) -> list[model]:
        data = await self._get_from_elastic_by_search(
            index=self.index, model=self.model, fields=["title"],
            search=search, page_size=page_size, page=page
        )
        return data


class BasePersonService(BaseService):
    model = Person

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        super().__init__(redis, elastic)
        self.index = "persons"

    async def _get_person_from_elastic(self, person_id: str) -> list[model]:
        query = {
            "query": {
                "match": {
                    "id": {
                        "query": person_id
                    }
                }
            }
        }

        try:
            doc = await self.elastic.search(index=self.index, body=query)
        except NotFoundError:
            return []

        data = []
        item = doc["hits"]["hits"][0]
        for role in PersonType:
            elastic_role = "{0}s".format(str(role.value))
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "nested": {
                                    "path": elastic_role,
                                    "query": {
                                        "match": {
                                            f"{elastic_role}.id": person_id
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            }

            try:
                doc2 = await self.elastic.search(index="movies", body=query)
                film_ids = [hit["_source"]['id']
                            for hit in doc2["hits"]["hits"]]
            except NotFoundError:
                film_ids = []

            data.append(
                Person(**item["_source"], film_ids=film_ids, role=role)
            )

        return data
