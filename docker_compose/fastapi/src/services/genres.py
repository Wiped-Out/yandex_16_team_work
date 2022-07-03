from functools import lru_cache
from typing import Optional

from fastapi import Depends

from db.db import get_elastic
from db.cache_db import get_redis
from models.genre import Genre
from services.base import BaseGenreService, AsyncCacheStorage, AsyncFullTextSearchStorage


class GenreService(BaseGenreService):
    async def get_genre(
            self,
            genre_id: str,
            cache_key: str
    ) -> Optional[Genre]:

        genre = await self.get_one_item_from_cache(cache_key=cache_key, model=Genre)

        if not genre:
            genre = await self.get_by_id(_id=genre_id, model=Genre, index=self.index)

            if genre:
                await self.put_one_item_to_cache(cache_key=cache_key, item=genre)

        return genre


class GenresService(BaseGenreService):
    async def get_genres(
            self,
            page: int,
            page_size: int,
            cache_key: str,
    ) -> list[Genre]:
        genres = await self.get_items_from_cache(cache_key=cache_key, model=Genre)

        if not genres:
            genres = await self.get_data(
                page_size=page_size, page=page, model=Genre, index=self.index
            )

            if genres:
                await self.put_items_to_cache(cache_key=cache_key, items=genres)

        return genres


@lru_cache()
def get_genre_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        full_text_search: AsyncFullTextSearchStorage = Depends(get_elastic)
) -> GenreService:
    return GenreService(cache=cache, full_text_search=full_text_search)


@lru_cache()
def get_genres_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        full_text_search: AsyncFullTextSearchStorage = Depends(get_elastic)
) -> GenresService:
    return GenresService(cache=cache, full_text_search=full_text_search)
