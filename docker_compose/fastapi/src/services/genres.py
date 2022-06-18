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
    async def get_genre(self, genre_id: str) -> Optional[Genre]:
        genre = await self._get_genre_from_cache(genre_id=genre_id)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id=genre_id)
            if genre:
                await self._put_genre_to_cache(genre=genre)
            return genre
        return genre

    async def _get_genre_from_cache(self, genre_id: str) -> Optional[Genre]:
        data = await self.redis.get(key=genre_id)
        if not data:
            return None
        return Genre.parse_raw(data)


class GenresService(BaseGenreService):
    async def get_genres(self) -> list[Genre]:
        genres = await self._get_genres_from_cache()
        if not genres:
            genres = await self._get_genres_from_elastic()
            if genres:
                await self._put_genres_to_cache(genres=genres)
            return genres
        return genres

    async def _get_genres_from_cache(self) -> list[Genre]:
        data = []
        for key in self.redis.scan("*"):
            data.append(Genre(**self.redis.get(key=key)))
        return data

    async def _put_genres_to_cache(self, genres: list[Genre]):
        for genre in genres:
            await self._put_genre_to_cache(genre=genre)


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
