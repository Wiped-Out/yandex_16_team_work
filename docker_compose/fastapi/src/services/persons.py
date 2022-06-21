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
    async def search_persons(
            self, search: str, page: int, page_size: int
    ) -> list[Person]:
        # todo
        # persons = await self._get_persons_from_cache_by_search(search=search)
        persons = []
        if not persons:
            persons = await self._search_persons_in_elastic(
                search=search, page_size=page_size, page=page
            )
            if persons:
                await self._put_persons_to_cache(persons=persons)
        return persons

    async def _get_persons_by_id(self, person_id: str) -> list[Person]:
        persons = await self._get_person_from_cache(person_id=person_id)
        if not persons:
            persons = await self._get_person_from_elastic(person_id=person_id)
            if persons:
                await self._put_persons_to_cache(persons=persons)
        return persons

    async def _get_persons_from_cache_by_search(
            self, search: str
    ) -> list[Person]:
        data = []

        keys = await self.redis.keys(pattern="*")
        for key in keys:
            person_from_redis = await self.redis.get(key)
            person = Person.parse_raw(person_from_redis)

            # Не подходит по поисковому запросу
            if search and \
                    not fuzz.WRatio(search.lower(), person.full_name) > 80:
                continue

            data.append(person)

        return data

    async def _search_persons_in_elastic(
            self, search: str, page: int, page_size: int
    ) -> list[Person]:
        # todo Добавить сюда наполнение модели фильмами и ролью
        data = await self._get_from_elastic_by_search(
            index=self.index, model=Person, fields=["full_name"],
            search=search, page_size=page_size, page=page
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
        data = []
        keys = await self.redis.keys(pattern="*")
        for key in keys:
            if key != person_id:
                continue

            person_from_redis = await self.redis.get(key)
            person = Person.parse_raw(person_from_redis)
            data.append(person)
        return data

    async def _put_persons_to_cache(self, persons: list[Person]):
        for person in persons:
            await self._put_person_to_cache(person=person)


@lru_cache()
def get_persons_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonsService:
    return PersonsService(redis=redis, elastic=elastic)
