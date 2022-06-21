from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from services.base import BaseGenreService
import json


class GenreService(BaseGenreService):
    async def get_genre(
            self, genre_id: str, cache_key: str
    ) -> Optional[Genre]:
        genre = await self._get_genre_from_cache(cache_key=cache_key)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id=genre_id)
            if genre:
                await self._put_genre_to_cache(genre=genre, cache_key=cache_key)
            return genre
        return genre

    async def _get_genre_from_cache(self, cache_key: str) -> Optional[Genre]:
        data = await self.redis.get(key=cache_key)
        if not data:
            return None
        return Genre.parse_raw(data)

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        return await self._get_from_elastic_by_id(
            _id=genre_id, index=self.index, model=self.model,
        )


class GenresService(BaseGenreService):
    async def get_genres(
            self, page: int, page_size: int, cache_key: str,
    ) -> list[Genre]:
        genres = await self._get_genres_from_cache(cache_key=cache_key)
        if not genres:
            genres = await self._get_genres_from_elastic(
                page_size=page_size, page=page,
            )
            if genres:
                await self._put_genres_to_cache(
                    genres=genres, cache_key=cache_key,
                )
            return genres
        return genres

    async def _get_genres_from_cache(self, cache_key: str) -> list[Genre]:
        data = await self.redis.get(key=cache_key)
        if not data:
            return []

        return [Genre.parse_raw(person_dict) for person_dict in json.loads(data)]

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

    async def _put_genres_to_cache(
            self, genres: list[Genre], cache_key: str,
    ):
        genres = [person.json() for person in genres]
        await self.redis.set(
            key=cache_key, value=json.dumps(genres),
            expire=self.CACHE_EXPIRE_IN_SECONDS,
        )


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
