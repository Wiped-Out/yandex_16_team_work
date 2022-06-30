from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from services.base import BaseFilmService


class FilmService(BaseFilmService):
    async def get_film_by_id(self, film_id: str, cache_key: str) -> Optional[Film]:

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
            cache_key: str,
            sort_param: Optional[str] = None,
            genre_id: Optional[str] = None,
            search: Optional[str] = None
    ) -> list[Film]:

        films = await self.get_items_from_cache(cache_key=cache_key, model=Film)

        if not films:
            films = await self._get_films_from_elastic(
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
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> FilmService:
    return FilmService(redis, elastic)


@lru_cache()
def get_films_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> FilmsService:
    return FilmsService(redis, elastic)
