from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from services.base import BaseGenreService, BaseRedisService


class GenreService(BaseGenreService, BaseRedisService):
    async def get_genre(
            self, genre_id: str, cache_key: str
    ) -> Optional[Genre]:
        genre = await self.get_one_item_from_cache(cache_key=cache_key, model=Genre)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id=genre_id)
            if genre:
                await self.put_one_item_to_cache(cache_key=cache_key, item=genre)
            return genre
        return genre

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        return await self._get_from_elastic_by_id(
            _id=genre_id, index=self.index, model=self.model,
        )


class GenresService(BaseGenreService, BaseRedisService):
    async def get_genres(
            self, page: int, page_size: int, cache_key: str,
    ) -> list[Genre]:
        genres = await self.get_items_from_cache(cache_key=cache_key, model=Genre)
        if not genres:
            genres = await self._get_genres_from_elastic(
                page_size=page_size, page=page,
            )
            if genres:
                await self.put_items_to_cache(cache_key=cache_key, items=genres)
            return genres
        return genres

    async def _get_genres_from_elastic(
            self, page: int, page_size: int,
    ) -> list[Genre]:
        return await self._get_all_data_from_elastic(
            index=self.index, model=self.model, page_size=page_size,
            page=page
        )

    async def count_genres_in_elastic(self) -> int:
        count = await self.elastic.count(index=self.index)
        return count["count"]


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
