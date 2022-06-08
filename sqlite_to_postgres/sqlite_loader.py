import sqlite3
from contextlib import closing
from dataclasses import dataclass
from typing import Tuple

from models import Filmwork, Person, Genre, GenreFilmwork, PersonFilmwork


@dataclass
class SQLiteLoader:
    """Класс для выгрузки данных из SQLite"""
    connection: sqlite3.Connection
    page_size: int = 500

    def get_filmworks(self) -> Tuple[Filmwork]:
        with closing(self.connection.cursor()) as curs:
            sql_query = """
            SELECT title, description, creation_date,
            created_at, updated_at, type, file_path, rating, id
            FROM film_work
            """
            curs.execute(sql_query)
            while results := curs.fetchmany(self.page_size):
                yield tuple(Filmwork(*i)
                            for i in results)

    def get_genres(self) -> Tuple[Genre]:
        with closing(self.connection.cursor()) as curs:
            sql_query = """
            SELECT name, description, created_at, updated_at, id
            FROM genre
            """
            curs.execute(sql_query)
            while results := curs.fetchmany(self.page_size):
                yield tuple(Genre(*i)
                            for i in results)

    def get_persons(self) -> Tuple[Person]:
        with closing(self.connection.cursor()) as curs:
            sql_query = """
            SELECT full_name, created_at, updated_at, id
            FROM person
            """
            curs.execute(sql_query)
            while results := curs.fetchmany(self.page_size):
                yield tuple(Person(*i)
                            for i in results)

    def get_genres_filmworks(self) -> Tuple[GenreFilmwork]:
        with closing(self.connection.cursor()) as curs:
            sql_query = """
            SELECT created_at, id, film_work_id, genre_id
            FROM genre_film_work
            """
            curs.execute(sql_query)
            while results := curs.fetchmany(self.page_size):
                yield tuple(GenreFilmwork(*i)
                            for i in results)

    def get_persons_filmworks(self) -> Tuple[PersonFilmwork]:
        with closing(self.connection.cursor()) as curs:
            sql_query = """
            SELECT role, created_at, id, film_work_id, person_id
            FROM person_film_work
            """
            curs.execute(sql_query)
            while results := curs.fetchmany(self.page_size):
                yield tuple(PersonFilmwork(*i)
                            for i in results)
