import json
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from elasticsearch import NotFoundError

from models.film import Film
from models.genre import Genre
from models.person import Person, PersonType


class BaseRedisService:
    def __init__(self, redis: Redis, **kwargs):
        super().__init__(**kwargs)

        self.redis = redis
        self.CACHE_EXPIRE_IN_SECONDS = 60 * 5

    async def get_one_item_from_cache(self, cache_key: str, model):
        data = await self.redis.get(key=cache_key)

        if not data:
            return None

        return model.parse_raw(data)

    async def put_one_item_to_cache(self, cache_key: str, item):
        await self.redis.set(
            key=cache_key,
            value=item.json(),
            expire=self.CACHE_EXPIRE_IN_SECONDS,
        )

    async def get_items_from_cache(self, cache_key: str, model):
        data = await self.redis.get(key=cache_key)
        if not data:
            return []

        return [model.parse_raw(item) for item in json.loads(data)]

    async def put_items_to_cache(self, cache_key: str, items: list):
        await self.redis.set(
            key=cache_key,
            value=json.dumps([item.json() for item in items]),
            expire=self.CACHE_EXPIRE_IN_SECONDS,
        )


class BaseElasticService:
    def __init__(self, elastic: AsyncElasticsearch, **kwargs):
        super().__init__(**kwargs)

        self.elastic = elastic

    async def get_by_id(
            self,
            _id: str,
            model,
            index: str
    ):
        try:
            doc = await self.elastic.get(index, _id)
        except NotFoundError:
            return None

        return model(**doc["_source"])

    async def get_data_from_elastic(
            self,
            page: int,
            page_size: int,
            model,
            index: str,
    ):
        query = {
            "query": {
                "match_all": {}
            }
        }

        try:
            doc = await self.elastic.search(
                index=index,
                body=query,
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
            self,
            search: str,
            fields: list[str],
            index: str,
            page: int,
            page_size: int,
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
                index=index,
                body=query,
                from_=page_size * (page - 1),
                size=page_size
            )
        except NotFoundError:
            return {}

        return doc

    async def get_items_by_search(
            self,
            search: str,
            fields: list[str],
            index: str,
            model,
            page: int,
            page_size: int
    ) -> list:
        doc = await self._search_in_elastic(
            search=search,
            fields=fields,
            index=index,
            page=page,
            page_size=page_size
        )

        if not doc:
            return []

        return [model(**item["_source"]) for item in doc["hits"]["hits"]]


class ElasticFilm(BaseElasticService):
    def __init__(self, elastic: AsyncElasticsearch, **kwargs):
        super(ElasticFilm, self).__init__(elastic=elastic, **kwargs)

        self.elastic = elastic
        self.index = "movies"
        self.model = Film

    async def _get_films_from_elastic(
            self,
            sort_param: Optional[str],
            search: Optional[str],
            genre_id: Optional[str],
            page: int,
            page_size: int
    ) -> list[Film]:
        if search:
            return await self.get_items_by_search(
                search=search, page_size=page_size, page=page,
                index=self.index, model=self.model, fields=["title"]
            )

        query = {
            "query": {
                "bool": {
                    "must": []
                }
            }
        }

        if genre_id:
            query["query"]["bool"]["must"].append(
                {
                    "nested": {
                        "path": "genre",
                        "query": {
                            "match": {
                                "genre.id": genre_id
                            }
                        }
                    }
                }
            )

        try:
            doc = await self.elastic.search(
                index=self.index,
                body=query,
                from_=page_size * (page - 1),
                sort="imdb_rating:desc"
                if sort_param == "-imdb_rating"
                else "imdb_rating:asc",

                size=page_size
            )
        except NotFoundError:
            return []

        return [Film(**film["_source"]) for film in doc["hits"]["hits"]]

    async def count_items_in_elastic(
            self,
            search: Optional[str] = None,
            genre_id: Optional[str] = None
    ) -> int:
        if search:
            query = {
                "query": {
                    "multi_match": {
                        "query": search,
                        "fields": ["title"],
                        "fuzziness": "auto"
                    }
                }
            }

            count = await self.elastic.count(index=self.index, body=query)
            return count["count"]

        query = {
            "query": {
                "bool": {
                    "must": []
                }
            }
        }

        if genre_id:
            query["query"]["bool"]["must"].append(
                {
                    "nested": {
                        "path": "genre",
                        "query": {
                            "match": {
                                "genre.id": genre_id
                            }
                        }
                    }
                }
            )

        count = await self.elastic.count(index=self.index, body=query)

        return count["count"]

    async def get_films_for_person_query(self, person_id: str) -> dict:
        query = {
            "query": {
                "bool": {
                    "should": []
                }
            }
        }

        for role in ("actors", "directors", "writers"):
            query["query"]["bool"]["should"].append({
                "nested": {
                    "path": role,
                    "query": {
                        "match": {
                            f"{role}.id": person_id,
                        }
                    }
                }
            })

        return query

    async def get_films_for_person(
            self,
            person_id: str,
            page: int,
            page_size: int
    ) -> list[Film]:

        query = await self.get_films_for_person_query(person_id=person_id)

        try:
            doc = await self.elastic.search(
                index=self.index,
                body=query,
                from_=page_size * (page - 1),
                size=page_size
            )

            return [Film(**item["_source"]) for item in doc["hits"]["hits"]]
        except NotFoundError:
            return []

    async def count_films_for_person_in_elastic(self, person_id: str) -> int:
        query = await self.get_films_for_person_query(person_id=person_id)
        count = await self.elastic.count(index=self.index, body=query)

        return count["count"]


class ElasticPerson(BaseElasticService):
    def __init__(self, elastic: AsyncElasticsearch, **kwargs):
        super().__init__(elastic=elastic, **kwargs)

        self.elastic = elastic
        self.index = "persons"

    async def search_persons_in_elastic(
            self,
            search: str,
            page: int,
            page_size: int
    ) -> list[Person]:

        doc = await self._search_in_elastic(
            search=search,
            fields=["full_name"],
            index=self.index,
            page=page,
            page_size=page_size
        )

        if not doc:
            return []

        data = []
        for item in doc["hits"]["hits"]:
            persons = await self.get_person_from_elastic(person_id=item["_source"]["id"])
            data += persons

        return data

    async def get_person_from_elastic(self, person_id: str) -> list:
        try:
            doc = await self.elastic.get(self.index, person_id)
        except NotFoundError:
            return []

        persons = await self.get_films_for_person_from_elastic(
            person_data=doc, person_id=person_id
        )
        return persons

    async def get_films_for_person_from_elastic(self, person_data: dict, person_id: str):
        persons = []
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
                film_ids = [hit["_source"]['id'] for hit in doc2["hits"]["hits"]]
            except NotFoundError:
                film_ids = []

            persons.append(Person(**person_data["_source"], film_ids=film_ids, role=role))

        return persons

    async def count_persons_in_elastic(self, search: str) -> int:
        query = {
            "query": {
                "multi_match": {
                    "query": search,
                    "fields": ["full_name"],
                    "fuzziness": "auto"
                }
            }
        }

        count = await self.elastic.count(index=self.index, body=query)
        return count["count"]


class BaseFilmService(BaseRedisService, ElasticFilm):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch, **kwargs):
        super().__init__(redis=redis, elastic=elastic, **kwargs)

        self.index = "movies"
        self.model = Film
        self.redis = redis
        self.elastic = elastic


class BasePersonService(BaseRedisService, ElasticPerson):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch, **kwargs):
        super().__init__(redis=redis, elastic=elastic, **kwargs)

        self.index = "persons"
        self.model = Person
        self.redis = redis
        self.elastic = elastic


class BaseGenreService(BaseRedisService, BaseElasticService):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch, **kwargs):
        super().__init__(redis=redis, elastic=elastic, **kwargs)

        self.index = "genres"
        self.model = Genre
        self.redis = redis
        self.elastic = elastic
