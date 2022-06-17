from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from fuzzywuzzy import fuzz

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class ServiceMixin:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(
            key=film.id, value=film.json(),
            expire=FILM_CACHE_EXPIRE_IN_SECONDS,
        )


class FilmService(ServiceMixin):
    async def get_by_id(self, film_id: str) -> Optional[Film]:
        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            # Сохраняем фильм в кеш
            await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get('movies', film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None

        film = Film.parse_raw(data)
        return film


class FilmsService(ServiceMixin):
    async def get_films(
            self, sort_param: Optional[str] = None,
            genre_id: Optional[str] = None,
            search: Optional[str] = None,
    ) -> list[Film]:
        films = await self._films_from_cache(sort_param=sort_param, search=search)
        if not films:
            films = await self._get_films_from_elastic(sort_param=sort_param, search=search)
            if films:
                await self._put_films_to_cache(films=films)
            return films

        return films

    async def _get_films_from_elastic(
            self, sort_param: Optional[str],
            search: Optional[str],
    ) -> list[Film]:
        # todo здесь я не уверен в запросе + не знаю как встроить поиск по жанру

        if search:
            query = {
                "query": {
                    "nested": {
                        "path": "genre",
                        "query": {
                            "bool": {
                                "must": [
                                    {"match_all": {"title": search}}
                                ]
                            }
                        }
                    }
                }
            }
        else:
            query = {
                "query": {
                    "nested": {
                        "path": "genre",
                        "query": {
                            "bool": {
                                "must": [
                                    {"match_all": {}}
                                ]
                            }
                        }
                    }
                }
            }

        count_rows = await self.elastic.count(index="movies")
        try:
            doc = await self.elastic.get(
                index="movies", body=query,
                sort="imdb_rating:desc" if sort_param == "-imdb_rating" else "imdb_rating:asc",
                size=count_rows["count"]
            )
        except NotFoundError:
            return []

        return [Film(**film) for film in doc["hits"]["hits"]]

    async def _films_from_cache(
            self, sort_param: Optional[str],
            search: Optional[str]
    ) -> list[Film]:
        data = []

        # Если есть поисковой запрос
        if search:
            for key in self.redis.keys(pattern="*"):
                film = Film(**self.redis.get(key))
                # Проверяем совпадение строк. Коэффициент больше 80
                # говорит о том, что этот фильм нам подходит
                if fuzz.WRatio(search.lower(), film.title) > 80:
                    data.append(film)

            return data

        for key in self.redis.keys(pattern="*"):
            data.append(Film(**self.redis.get(key)))

        # Если добавлен запрос на сортировку
        if sort_param:
            data.sort(
                key=lambda x: x.imdb_rating,
                reverse=sort_param == "-imdb_rating"
            )
        return data

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
