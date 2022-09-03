from functools import lru_cache
from typing import List

from db.cache_db import get_cache_db
from db.db import get_db
from fastapi import Depends
from models.person import Person
from services.base import (AsyncCacheStorage, AsyncFullTextSearchStorage,
                           BaseSearchPersonService)


class PersonsService(BaseSearchPersonService):
    async def search_persons(
            self,
            search: str,
            page: int,
            page_size: int,
            base_url: str,
    ) -> List[Person]:
        cache_key = f'{base_url}_search={search}_page_size={page_size}_page={page}'
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
            base_url: str,
    ) -> List[Person]:

        cache_key = f'{base_url}_person_id={person_id}'
        persons = await self.get_items_from_cache(
            cache_key=cache_key,
            model=self.model,
        )

        if not persons:
            persons = await self.get_person(person_id=person_id)

            if persons:
                await self.put_items_to_cache(cache_key=cache_key, items=persons)

        return persons


@lru_cache()
def get_persons_service(
        cache: AsyncCacheStorage = Depends(get_cache_db),
        full_text_search: AsyncFullTextSearchStorage = Depends(get_db),
) -> PersonsService:
    return PersonsService(cache=cache, full_text_search=full_text_search)
