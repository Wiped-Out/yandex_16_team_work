from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person
from services.base import BasePersonService, AsyncCacheStorage


class PersonsService(BasePersonService):
    async def search_persons(
            self,
            search: str,
            page: int,
            page_size: int,
            cache_key: str
    ) -> list[Person]:
        persons = await self.get_items_from_cache(cache_key=cache_key, model=Person)

        if not persons:
            persons = await self.search_persons_in_elastic(
                search=search,
                page_size=page_size,
                page=page
            )

            if persons:
                await self.put_items_to_cache(cache_key=cache_key, items=persons)

        return persons

    async def _get_persons_by_id(
            self,
            person_id: str,
            cache_key: str
    ) -> list[Person]:

        persons = await self.get_items_from_cache(
            cache_key=cache_key,
            model=self.model
        )

        if not persons:
            persons = await self.get_person_from_elastic(person_id=person_id)

            if persons:
                await self.put_items_to_cache(cache_key=cache_key, items=persons)

        return persons


@lru_cache()
def get_persons_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> PersonsService:
    return PersonsService(cache=cache, elastic=elastic)
