from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person
from fuzzywuzzy import fuzz

PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class BasePersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.index = "persons"

    async def _put_person_to_cache(self, person: Person):
        await self.redis.set(
            key=str(person.uuid), value=person.json(),
            expire=PERSON_CACHE_EXPIRE_IN_SECONDS,
        )


class PersonService(BasePersonService):
    async def get_person(self, person_id: str) -> Optional[Person]:
        person = await self._get_person_from_cache(person_id=person_id)
        if not person:
            person = await self._get_person_from_elastic(person_id=person_id)
            if person:
                await self._put_person_to_cache(person=person)
        return person

    async def _get_person_from_elastic(self, person_id: str) -> Optional[Person]:
        try:
            doc = await self.elastic.get(self.index, person_id)
        except NotFoundError:
            return None

        return Person(**doc["_source"])

    async def _get_person_from_cache(
            self, person_id: str
    ) -> Optional[Person]:
        data = await self.redis.get(key=person_id)
        if not data:
            return None
        return Person(**data)


class PersonsService(BasePersonService):
    async def get_persons(
            self, search_param: Optional[str] = None,
    ) -> list[Person]:
        # persons = await self._get_persons_from_cache(search_param=search_param)
        persons = []
        if not persons:
            persons = await self._get_persons_from_elastic(search_param=search_param)
            if persons:
                await self._put_persons_to_cache(persons=persons)
        return persons

    async def _get_persons_from_elastic(
            self, search_param: Optional[str] = None
    ) -> list[Person]:
        if search_param:
            query = {
                "query": {
                    "multi_match": {
                        "query": search_param,
                        "fields": ["full_name"],
                        "fuzziness": "auto"
                    }
                }
            }
        else:
            query = {
                "query": {
                    "nested": {
                        "path": "genre",
                        "query": {
                            "bool": {
                                "must": [
                                    {"match_all": {}}
                                ]
                            }
                        }
                    }
                }
            }

        try:
            doc = await self.elastic.search(
                index=self.index,
                body=query,
            )
            print(f"То что вытащил {doc}")

            return [Person(**person["_source"]) for person in doc["hits"]["hits"]]
        except NotFoundError:
            return []

    async def _get_persons_from_cache(
            self, search_param: Optional[str] = None,
    ) -> list[Person]:
        data = []

        if search_param:
            for key in self.redis.keys("*"):
                person = Person(**self.redis.get(key=key))
                if fuzz.WRatio(
                        search_param.lower(), person.full_name.lower()
                ) > 80:
                    data.append(person)

            return data

        for key in self.redis.keys("*"):
            data.append(Person(**self.redis.get(key=key)))

        return data

    async def _put_persons_to_cache(self, persons: list[Person]):
        for person in persons:
            await self._put_person_to_cache(person=person)


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis=redis, elastic=elastic)


@lru_cache()
def get_persons_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonsService:
    return PersonsService(redis=redis, elastic=elastic)
