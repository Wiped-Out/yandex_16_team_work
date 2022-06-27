from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person, PersonType
from services.base import BasePersonService, BaseRedisService


class PersonsService(BasePersonService, BaseRedisService):
    async def search_persons(
            self, search: str, page: int, page_size: int,
            cache_key: str,
    ) -> list[Person]:
        persons = await self.get_items_from_cache(cache_key=cache_key, model=Person)
        if not persons:
            persons = await self._search_persons_in_elastic(
                search=search, page_size=page_size, page=page
            )
            if persons:
                await self.put_items_to_cache(cache_key=cache_key, items=persons)
        return persons

    async def _get_persons_by_id(
            self, person_id: str, cache_key: str,
    ) -> list[Person]:
        persons = await self._get_person_from_cache(person_id=person_id)
        if not persons:
            persons = await self._get_person_from_elastic(person_id=person_id)
            if persons:
                await self.put_items_to_cache(cache_key=cache_key, items=persons)
        return persons

    async def _search_persons_in_elastic(
            self, search: str, page: int, page_size: int
    ) -> list[Person]:
        query = {
            "query": {
                "multi_match": {
                    "query": search,
                    "fields": ["full_name"],
                    "fuzziness": "auto"
                }
            }
        }

        try:
            doc = await self.elastic.search(
                index=self.index, body=query,
                from_=page_size * (page - 1),
                size=page_size
            )
        except NotFoundError:
            return []

        data = []
        for item in doc["hits"]["hits"]:
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
                                                f"{elastic_role}.id": item["_source"]["id"]
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

    async def _get_person_from_cache(self, person_id: str) -> list[Person]:
        # todo зачем мы сделали именно таким сложным образом?
        data = []
        keys = await self.redis.keys(pattern="*")
        for key in keys:
            if key != person_id:
                continue

            person_from_redis = await self.redis.get(key)
            person = Person.parse_raw(person_from_redis)
            data.append(person)
        return data


@lru_cache()
def get_persons_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonsService:
    return PersonsService(redis=redis, elastic=elastic)
