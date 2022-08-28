from typing import Optional

from elasticsearch import NotFoundError
from models.film import Film
from models.genre import Genre
from models.person import Person, PersonType
from services.base_cache import AsyncCacheStorage, BaseCacheStorage
from services.base_full_text_search import (AsyncFullTextSearchStorage,
                                            BaseFullTextSearchStorage)


class FullTextSearchFilm(BaseFullTextSearchStorage):
    def __init__(self, full_text_search: AsyncFullTextSearchStorage, **kwargs):
        super(FullTextSearchFilm, self).__init__(full_text_search=full_text_search, **kwargs)

        self.full_text_search = full_text_search
        self.index = 'movies'
        self.model = Film

    async def get_films_from_db(
            self,
            sort_param: Optional[str],
            search: Optional[str],
            genre_id: Optional[str],
            page: int,
            page_size: int,
    ) -> list[Film]:
        if search:
            return await self.get_items_by_search(
                search=search, page_size=page_size, page=page,
                index=self.index, model=self.model, fields=['title'],
            )

        query = {
            'query': {
                'bool': {
                    'must': [],
                },
            },
        }

        if genre_id:
            query['query']['bool']['must'].append(
                {
                    'nested': {
                        'path': 'genre',
                        'query': {
                            'match': {
                                'genre.id': genre_id,
                            },
                        },
                    },
                },
            )

        try:
            doc = await self.full_text_search.search(
                index=self.index,
                body=query,
                from_=page_size * (page - 1),
                sort='imdb_rating:desc'
                if sort_param == '-imdb_rating'
                else 'imdb_rating:asc',
                size=page_size,
            )
        except NotFoundError:
            return []

        return [Film(**film['_source']) for film in doc['hits']['hits']]

    async def count_items(
            self,
            search: Optional[str] = None,
            genre_id: Optional[str] = None,
    ) -> int:
        if search:
            query = {
                'query': {
                    'multi_match': {
                        'query': search,
                        'fields': ['title'],
                        'fuzziness': 'auto',
                    },
                },
            }

            count = await self.full_text_search.count(index=self.index, body=query)
            return count['count']

        query = {
            'query': {
                'bool': {
                    'must': [],
                },
            },
        }

        if genre_id:
            query['query']['bool']['must'].append(
                {
                    'nested': {
                        'path': 'genre',
                        'query': {
                            'match': {
                                'genre.id': genre_id,
                            },
                        },
                    },
                },
            )

        count = await self.full_text_search.count(index=self.index, body=query)

        return count['count']

    async def get_films_for_person_query(self, person_id: str) -> dict:
        query = {
            'query': {
                'bool': {
                    'should': [],
                },
            },
        }

        for role in ('actors', 'directors', 'writers'):
            query['query']['bool']['should'].append({
                'nested': {
                    'path': role,
                    'query': {
                        'match': {
                            f'{role}.id': person_id,
                        },
                    },
                },
            })

        return query

    async def get_films_for_person(
            self,
            person_id: str,
            page: int,
            page_size: int,
    ) -> list[Film]:

        query = await self.get_films_for_person_query(person_id=person_id)

        try:
            doc = await self.full_text_search.search(
                index=self.index,
                body=query,
                from_=page_size * (page - 1),
                size=page_size,
            )

            return [Film(**item['_source']) for item in doc['hits']['hits']]
        except NotFoundError:
            return []

    async def count_films_for_person(self, person_id: str) -> int:
        query = await self.get_films_for_person_query(person_id=person_id)
        count = await self.full_text_search.count(index=self.index, body=query)

        return count['count']


class BaseFilmService(BaseCacheStorage, FullTextSearchFilm):
    def __init__(
            self,
            cache: AsyncCacheStorage,
            full_text_search: AsyncFullTextSearchStorage,
            **kwargs,
    ):
        super().__init__(cache=cache, full_text_search=full_text_search, **kwargs)

        self.index = 'movies'
        self.model = Film


class FullTextSearchPerson(BaseFullTextSearchStorage):
    def __init__(self, full_text_search: AsyncFullTextSearchStorage, **kwargs):
        super().__init__(full_text_search=full_text_search, **kwargs)

        self.full_text_search = full_text_search
        self.index = 'persons'

    async def search_persons_in_db(
            self,
            search: str,
            page: int,
            page_size: int,
    ) -> list[Person]:

        doc = await self.search(
            search=search,
            fields=['full_name'],
            index=self.index,
            page=page,
            page_size=page_size,
        )

        if not doc:
            return []

        data = []
        for item in doc['hits']['hits']:
            persons = await self.get_person(person_id=item['_source']['id'])
            data += persons

        return data

    async def get_person(self, person_id: str) -> list:
        try:
            doc = await self.full_text_search.get(self.index, person_id)
        except NotFoundError:
            return []

        persons = await self.get_films_for_person(
            person_data=doc, person_id=person_id,
        )
        return persons

    async def get_films_for_person(self, person_data: dict, person_id: str):
        persons = []
        for role in PersonType:
            role_in_query = '{0}s'.format(str(role.value))
            query = {
                'query': {
                    'bool': {
                        'must': [
                            {
                                'nested': {
                                    'path': role_in_query,
                                    'query': {
                                        'match': {
                                            f'{role_in_query}.id': person_id,
                                        },
                                    },
                                },
                            },
                        ],
                    },
                },
            }

            try:
                doc2 = await self.full_text_search.search(index='movies', body=query)
                film_ids = [hit['_source']['id'] for hit in doc2['hits']['hits']]
            except NotFoundError:
                film_ids = []

            persons.append(Person(**person_data['_source'], film_ids=film_ids, role=role))

        return persons

    async def count_persons(self, search: str) -> int:
        query = {
            'query': {
                'multi_match': {
                    'query': search,
                    'fields': ['full_name'],
                    'fuzziness': 'auto',
                },
            },
        }

        count = await self.full_text_search.count(index=self.index, body=query)
        return count['count']


class BaseSearchPersonService(BaseCacheStorage, FullTextSearchPerson):
    def __init__(
            self,
            cache: AsyncCacheStorage,
            full_text_search: AsyncFullTextSearchStorage,
            **kwargs,
    ):
        super().__init__(cache=cache, full_text_search=full_text_search, **kwargs)

        self.index = 'persons'
        self.model = Person


class BaseGenreService(BaseCacheStorage, BaseFullTextSearchStorage):
    def __init__(
            self,
            cache: AsyncCacheStorage,
            full_text_search: AsyncFullTextSearchStorage,
            **kwargs,
    ):
        super().__init__(cache=cache, full_text_search=full_text_search, **kwargs)

        self.index = 'genres'
        self.model = Genre
