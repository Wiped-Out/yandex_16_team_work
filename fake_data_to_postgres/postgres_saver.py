from dataclasses import dataclass
from typing import Tuple

from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch

from models import Filmwork, Person, Genre, GenreFilmwork, PersonFilmwork


@dataclass
class PostgresSaver:
    """Класс для загрузки данных в PostgreSQL"""
    pgconn: _connection
    page_size: int = 500

    def save_filmworks(self, filmworks: Tuple[Filmwork]):
        with self.pgconn.cursor() as cur:
            sql_query = """
            INSERT INTO content.film_work
            (title, description, creation_date,
            created, modified, type, file_path, rating, id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
            """
            unpacked_filmworks = tuple(tuple(i) for i in filmworks)
            execute_batch(cur, sql_query, unpacked_filmworks,
                          page_size=self.page_size)

    def save_genres(self, genres: Tuple[Genre]):
        with self.pgconn.cursor() as cur:
            sql_query = """
            INSERT INTO content.genre
            (name, description, created, modified, id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
            """
            unpacked_genres = tuple(tuple(i) for i in genres)
            execute_batch(cur, sql_query, unpacked_genres,
                          page_size=self.page_size)

    def save_persons(self, persons: Tuple[Person]):
        with self.pgconn.cursor() as cur:
            sql_query = """
            INSERT INTO content.person
            (full_name, created, modified, id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
            """
            unpacked_persons = tuple(tuple(i) for i in persons)
            execute_batch(cur, sql_query, unpacked_persons,
                          page_size=self.page_size)

    def save_genres_filmworks(self, genres_filmworks: Tuple[GenreFilmwork]):
        with self.pgconn.cursor() as cur:
            sql_query = """
            INSERT INTO content.genre_film_work
            (created, id, film_work_id, genre_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """
            unpacked_genres_filmworks = \
                tuple(tuple(i) for i in genres_filmworks)
            execute_batch(cur, sql_query, unpacked_genres_filmworks,
                          page_size=self.page_size)

    def save_persons_filmworks(self, persons_filmworks: Tuple[PersonFilmwork]):
        with self.pgconn.cursor() as cur:
            sql_query = """
            INSERT INTO content.person_film_work
            (role, created, id, film_work_id, person_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """
            unpacked_persons_filmworks = \
                tuple(tuple(i) for i in persons_filmworks)
            execute_batch(cur, sql_query, unpacked_persons_filmworks,
                          page_size=self.page_size)
