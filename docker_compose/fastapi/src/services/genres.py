from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from services.base import BaseGenreService


class GenreService(BaseGenreService):
    async def get_genre(
            self, genre_id: str, cache_key: str
    ) -> Optional[Genre]:
        genre = await self.get_one_item_from_cache(cache_key=cache_key, model=Genre)
        if not genre:
            genre = await self.get_by_id(_id=genre_id, model=Genre, index=self.index)
            if genre:
                await self.put_one_item_to_cache(cache_key=cache_key, item=genre)
        return genre


class GenresService(BaseGenreService):
    async def get_genres(
            self, page: int, page_size: int, cache_key: str,
    ) -> list[Genre]:
        genres = await self.get_items_from_cache(cache_key=cache_key, model=Genre)
        if not genres:
            genres = await self.get_data_from_elastic(
                page_size=page_size, page=page, model=Genre, index=self.index
            )
            if genres:
                await self.put_items_to_cache(cache_key=cache_key, items=genres)
        return genres


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis=redis, elastic=elastic)


@lru_cache()
def get_genres_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> GenresService:
    return GenresService(redis=redis, elastic=elastic)
