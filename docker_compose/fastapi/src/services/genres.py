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
        # todo
        # genre = await self._get_genre_from_cache(genre_id=genre_id)
        genre = None
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

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        return await self._get_from_elastic_by_id(
            _id=genre_id, index=self.index, model=self.model,
        )


class GenresService(BaseGenreService):
    async def get_genres(self, page: int, page_size: int) -> list[Genre]:
        # todo
        # genres = await self._get_genres_from_cache()
        genres = []
        if not genres:
            genres = await self._get_genres_from_elastic(
                page_size=page_size, page=page,
            )
            if genres:
                await self._put_genres_to_cache(genres=genres)
            return genres
        return genres

    async def _get_genres_from_cache(self) -> list[Genre]:
        data = []
        keys = await self.redis.keys(pattern="*")
        for key in keys:
            genre_from_redis = await self.redis.get(key)
            genre = Genre.parse_raw(genre_from_redis)
            data.append(genre)

        return data

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
