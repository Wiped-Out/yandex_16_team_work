from functools import lru_cache

from fastapi import Depends

from db.db import get_elastic
from db.cache_db import get_redis
from models.person import Person
from services.base import BaseSearchPersonService, AsyncCacheStorage, AsyncFullTextSearchStorage


class PersonsService(BaseSearchPersonService):
    async def search_persons(
            self,
            search: str,
            page: int,
            page_size: int,
            cache_key: str
    ) -> list[Person]:
        persons = await self.get_items_from_cache(cache_key=cache_key, model=Person)

        if not persons:
            persons = await self.search_persons_in_db(
                search=search,
                page_size=page_size,
                page=page,
            )

            if persons:
                await self.put_items_to_cache(cache_key=cache_key, items=persons)

        return persons

    async def get_persons_by_id(
            self,
            person_id: str,
            cache_key: str
    ) -> list[Person]:

        persons = await self.get_items_from_cache(
            cache_key=cache_key,
            model=self.model
        )

        if not persons:
            persons = await self.get_person(person_id=person_id)

            if persons:
                await self.put_items_to_cache(cache_key=cache_key, items=persons)

        return persons


@lru_cache()
def get_persons_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        full_text_search: AsyncFullTextSearchStorage = Depends(get_elastic)
) -> PersonsService:
    return PersonsService(cache=cache, full_text_search=full_text_search)
