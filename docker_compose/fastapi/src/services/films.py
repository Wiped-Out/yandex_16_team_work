from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from fuzzywuzzy import fuzz
from services.base import BaseMovieService


class FilmService(BaseMovieService):
    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            # Сохраняем фильм в кеш
            await self._put_film_to_cache(film)

        return film

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None

        return Film.parse_raw(data)


class FilmsService(BaseMovieService):
    async def get_films(
            self, page_size: int, page: int,
            sort_param: Optional[str] = None,
            genre_id: Optional[str] = None,
            search: Optional[str] = None,
    ) -> list[Film]:
        films = await self._films_from_cache(
            sort_param=sort_param, search=search, genre_id=genre_id,
        )
        if not films:
            films = await self._get_films_from_elastic(
                sort_param=sort_param, search=search, genre_id=genre_id,
                page=page, page_size=page_size,
            )
            if films:
                await self._put_films_to_cache(films=films)
            return films

        return films

    async def _films_from_cache(
            self, sort_param: Optional[str],
            search: Optional[str], genre_id: Optional[str]
    ) -> list[Film]:
        data = []

        keys = await self.redis.keys(pattern="*")
        for key in keys:
            film_from_redis = await self.redis.get(key)
            film = Film.parse_raw(film_from_redis)

            # Не проходит фильтрацию по жанру
            if genre_id and not \
                    any(item.id == genre_id for item in film.genre):
                continue

            # Не подходит по поисковому запросу
            if search and not fuzz.WRatio(search.lower(), film.title) > 80:
                continue

            data.append(film)

        # Если добавлен запрос на сортировку
        if sort_param:
            data.sort(
                key=lambda x: x.imdb_rating,
                reverse=sort_param == "-imdb_rating"
            )
        return data

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

    async def _put_films_to_cache(self, films: list[Film]):
        for film in films:
            await self._put_film_to_cache(film=film)


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
