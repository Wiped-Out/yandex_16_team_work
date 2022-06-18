from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person
from fuzzywuzzy import fuzz
from services.base import BasePersonService


class PersonsService(BasePersonService):
    async def search_persons(self, search: str) -> list[Person]:
        persons = await self._get_persons_from_cache_by_search(search=search)
        if not persons:
            persons = await self._search_persons_in_elastic(search=search)
            if persons:
                await self._put_persons_to_cache(persons=persons)
        return persons

    async def get_persons_by_id(self, person_id: str) -> list[Person]:
        persons = await self._get_person_from_cache(person_id=person_id)
        if not persons:
            persons = await self._get_person_from_elastic(person_id=person_id)
            if persons:
                await self._put_persons_to_cache(persons=persons)
        return persons

    async def _get_persons_from_cache_by_search(self, search: str) -> list[Person]:
        data = []

        if search:
            for key in self.redis.keys("*"):
                person = Person(**self.redis.get(key=key))
                if fuzz.WRatio(
                        search.lower(), person.full_name.lower()
                ) > 80:
                    data.append(person)

            return data

        for key in self.redis.keys("*"):
            data.append(Person(**self.redis.get(key=key)))

        return data

    async def _get_person_from_cache(self, person_id: str) -> list[Person]:
        data = await self.redis.get(key=person_id)
        if not data:
            return []
        return [Person.parse_raw(person) for person in data]

    async def _put_persons_to_cache(self, persons: list[Person]):
        for person in persons:
            await self._put_person_to_cache(person=person)


@lru_cache()
def get_persons_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonsService:
    return PersonsService(redis=redis, elastic=elastic)
