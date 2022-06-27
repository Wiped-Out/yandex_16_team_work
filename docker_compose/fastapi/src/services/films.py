from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from services.base import BaseMovieService, BaseRedisService


class FilmService(BaseMovieService, BaseRedisService):
    async def get_by_id(self, film_id: str, cache_key: str) -> Optional[Film]:
        film = await self.get_one_item_from_cache(cache_key=cache_key, model=Film)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            # Сохраняем фильм в кеш
            await self.put_one_item_to_cache(cache_key=cache_key, item=film)

        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        return await self._get_from_elastic_by_id(
            _id=film_id, model=self.model, index=self.index
        )


class FilmsService(BaseMovieService, BaseRedisService):
    async def get_films(
            self, page_size: int, page: int,
            cache_key: str,
            sort_param: Optional[str] = None,
            genre_id: Optional[str] = None,
            search: Optional[str] = None,
    ) -> list[Film]:
        films = await self.get_items_from_cache(cache_key=cache_key, model=Film)
        if not films:
            films = await self._get_films_from_elastic(
                sort_param=sort_param, search=search, genre_id=genre_id,
                page=page, page_size=page_size,
            )
            if films:
                await self.put_items_to_cache(cache_key=cache_key, items=films)
            return films

        return films

    async def _get_films_from_elastic(
            self, sort_param: Optional[str],
            search: Optional[str], genre_id: Optional[str],
            page: int, page_size: int,
    ) -> list[Film]:

        if search:
            return await self._search_films_in_elastic(
                search=search, page_size=page_size, page=page
            )

        query = {
            "query": {
                "bool": {
                    "must": []
                }
            }
        }

        if genre_id:
            query["query"]["bool"]["must"].append(
                {
                    "nested": {
                        "path": "genre",
                        "query": {
                            "match": {
                                "genre.id": genre_id
                            }
                        }
                    }
                }
            )

        try:
            doc = await self.elastic.search(
                index=self.index, body=query,
                from_=page_size * (page - 1),
                sort="imdb_rating:desc"
                if sort_param == "-imdb_rating"
                else "imdb_rating:asc",
                size=page_size,
            )
        except NotFoundError:
            return []

        return [Film(**film["_source"]) for film in doc["hits"]["hits"]]

    async def count_items_in_elastic(
            self, search: Optional[str] = None, genre_id: Optional[str] = None
    ) -> int:
        if search:
            query = {
                "query": {
                    "multi_match": {
                        "query": search,
                        "fields": ["title"],
                        "fuzziness": "auto"
                    }
                }
            }

            count = await self.elastic.count(index=self.index, body=query)
            return count["count"]

        query = {
            "query": {
                "bool": {
                    "must": []
                }
            }
        }

        if genre_id:
            query["query"]["bool"]["must"].append(
                {
                    "nested": {
                        "path": "genre",
                        "query": {
                            "match": {
                                "genre.id": genre_id
                            }
                        }
                    }
                }
            )

        count = await self.elastic.count(index=self.index, body=query)
        return count["count"]

    async def get_films_for_person(
            self, person_id: str, page: int, page_size: int
    ) -> list[Film]:
        query = {
            "query": {
                "bool": {
                    "should": []
                }
            }
        }
        for role in ("actors", "directors", "writers"):
            query["query"]["bool"]["should"].append({
                "nested": {
                    "path": role,
                    "query": {
                        "match": {
                            f"{role}.id": person_id,
                        }
                    }
                }
            })

        try:
            doc = await self.elastic.search(
                index=self.index, body=query,
                from_=page_size * (page - 1),
                size=page_size,
            )
            return [Film(**item["_source"]) for item in doc["hits"]["hits"]]
        except NotFoundError:
            return []

    async def count_films_for_person_in_elastic(self, person_id: str) -> int:
        query = {
            "query": {
                "bool": {
                    "should": []
                }
            }
        }
        for role in ("actors", "directors", "writers"):
            query["query"]["bool"]["should"].append({
                "nested": {
                    "path": role,
                    "query": {
                        "match": {
                            f"{role}.id": person_id,
                        }
                    }
                }
            })

        count = await self.elastic.count(index=self.index, body=query)
        return count["count"]


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)


@lru_cache()
def get_films_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmsService:
    return FilmsService(redis, elastic)
