from dataclasses import dataclass

from models import Genres, Movies, Persons
from psycopg2.extensions import connection as _connection
from state_controller import StateController


@dataclass
class PostgresExtractor:
    """Класс для выгрузки данных из PostgreSQL"""

    pgconn: _connection
    pg_sc: StateController
    page_size: int = 500

    def extract_movies(self):
        with self.pgconn.cursor(name='etl_{id}'.format(id=id(self))) as cur:
            sql_query = """
            SELECT
               fw.id,
               fw.rating,
               COALESCE (
                   JSON_AGG(
                           DISTINCT jsonb_build_object(
                               'id', g.id,
                               'name', g.name
                         )
                        ) FILTER(WHERE pfw.role = 'writer'),
                   '[]'
               ) genre,
               fw.title,
               fw.description,
               COALESCE (
                   JSON_AGG(
                           DISTINCT jsonb_build_object(
                               'id', p.id,
                               'full_name', p.full_name
                         )
                        ) FILTER(WHERE pfw.role = 'director'),
                   '[]'
               )  directors,
               COALESCE (
                        ARRAY_AGG(DISTINCT p.full_name)
                        FILTER(WHERE pfw.role = 'actor'),
                        '{}'
               ) actors_names,
               COALESCE (
                        ARRAY_AGG(DISTINCT p.full_name)
                        FILTER(WHERE pfw.role = 'writer'),
                        '{}'
               ) writers_names,
               COALESCE (
                        ARRAY_AGG(DISTINCT p.full_name)
                        FILTER(WHERE pfw.role = 'director'),
                        '{}'
               ) directors_names,
               COALESCE (
                   JSON_AGG(
                           DISTINCT jsonb_build_object(
                               'id', p.id,
                               'full_name', p.full_name
                         )
                        ) FILTER(WHERE pfw.role = 'actor'),
                   '[]'
               ) actors,
               COALESCE (
                   JSON_AGG(
                           DISTINCT jsonb_build_object(
                               'id', p.id,
                               'full_name', p.full_name
                         )
                        ) FILTER(WHERE pfw.role = 'writer'),
                   '[]'
               ) writers
            FROM content.film_work fw
            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
            LEFT JOIN content.person p ON p.id = pfw.person_id
            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
            LEFT JOIN content.genre g ON g.id = gfw.genre_id
            WHERE fw.id IN
            (
            SELECT DISTINCT gfw.film_work_id
            FROM content.genre g
            LEFT JOIN content.genre_film_work gfw ON g.id = gfw.genre_id
            WHERE g.modified > %s

            UNION

            SELECT DISTINCT pfw.film_work_id
            FROM content.person p
            LEFT JOIN content.person_film_work pfw ON p.id = pfw.person_id
            WHERE p.modified > %s
            )
            OR fw.modified > %s
            GROUP BY fw.id
            OFFSET %s
            """

            self.pg_sc.get_state()

            cur.execute(sql_query, (self.pg_sc.timestamp,
                                    self.pg_sc.timestamp,
                                    self.pg_sc.timestamp,
                                    self.pg_sc.state))
            results = cur.fetchmany(self.page_size)
            while results:
                yield tuple(Movies(*i) for i in results)

    def extract_persons(self):
        with self.pgconn.cursor(name='etl_{id}'.format(id=id(self))) as cur:
            sql_query = """
            SELECT
               p.id,
               p.full_name
            FROM content.person p
            WHERE p.modified > %s
            OFFSET %s
            """

            self.pg_sc.get_state()

            cur.execute(sql_query, (self.pg_sc.timestamp,
                                    self.pg_sc.state))
            while results := cur.fetchmany(self.page_size):
                yield tuple(Persons(*i) for i in results)

    def extract_genres(self):
        with self.pgconn.cursor(name='etl_{id}'.format(id=id(self))) as cur:
            sql_query = """
            SELECT
               g.id,
               g.name
            FROM content.genre g
            WHERE g.modified > %s
            OFFSET %s
            """
            self.pg_sc.get_state()

            cur.execute(sql_query, (self.pg_sc.timestamp,
                                    self.pg_sc.state))
            while results := cur.fetchmany(self.page_size):
                yield tuple(Genres(*i)
                            for i in results)
