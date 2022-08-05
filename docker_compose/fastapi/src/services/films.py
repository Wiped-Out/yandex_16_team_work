from functools import lru_cache
from typing import Optional

from fastapi import Depends

from db.db import get_db
from db.cache_db import get_cache_db
from models.film import Film
from services.base import BaseFilmService, AsyncCacheStorage, AsyncFullTextSearchStorage


class FilmService(BaseFilmService):
    async def get_film_by_id(self, film_id: str, base_url: str) -> Optional[Film]:

        cache_key = f"{base_url}_{film_id=}"
        film = await self.get_one_item_from_cache(cache_key=cache_key, model=Film)

        if not film:
            film = await self.get_by_id(film_id, model=Film, index=self.index)

            if film:
                await self.put_one_item_to_cache(cache_key=cache_key, item=film)

        return film


class FilmsService(BaseFilmService):
    async def get_films(
            self,
            page_size: int,
            page: int,
            base_url: str,
            sort_param: Optional[str] = None,
            genre_id: Optional[str] = None,
            search: Optional[str] = None
    ) -> list[Film]:

        if search:
            cache_key = f"{base_url}_{search=}_{page_size=}_{page=}"
        else:
            cache_key = f"{base_url}_{sort_param=}_{page_size=}_{page=}"

        films = await self.get_items_from_cache(cache_key=cache_key, model=Film)

        if not films:
            films = await self.get_films_from_db(
                sort_param=sort_param,
                search=search,
                genre_id=genre_id,
                page=page,
                page_size=page_size,
            )

            if films:
                await self.put_items_to_cache(cache_key=cache_key, items=films)

        return films


@lru_cache()
def get_film_service(
        cache: AsyncCacheStorage = Depends(get_cache_db),
        full_text_search: AsyncFullTextSearchStorage = Depends(get_db)
) -> FilmService:
    return FilmService(cache=cache, full_text_search=full_text_search)


@lru_cache()
def get_films_service(
        cache: AsyncCacheStorage = Depends(get_cache_db),
        full_text_search: AsyncFullTextSearchStorage = Depends(get_db)
) -> FilmsService:
    return FilmsService(cache=cache, full_text_search=full_text_search)
