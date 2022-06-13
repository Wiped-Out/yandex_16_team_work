from dataclasses import dataclass
from typing import Tuple

from psycopg2.extensions import connection as _connection

from models import Movies, Persons
from state_controller import StateController


@dataclass
class PostgresExtractor:
    """Класс для выгрузки данных из PostgreSQL"""
    pgconn: _connection
    pg_sc: StateController
    page_size: int = 500

    def extract_movies(self) -> Tuple[Movies]:
        with self.pgconn.cursor() as cur:
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
            ORDER BY fw.modified
            OFFSET %s
            """

            self.pg_sc.get_state()

            cur.execute(sql_query, (self.pg_sc.timestamp,
                                    self.pg_sc.timestamp,
                                    self.pg_sc.timestamp,
                                    self.pg_sc.state))
            while results := cur.fetchmany(self.page_size):
                yield tuple(Movies(*i)
                            for i in results)

    def extract_persons(self, role: str) -> Tuple[Persons]:
        with self.pgconn.cursor() as cur:
            sql_query = """
            SELECT
               p.id,
               p.full_name,
               pfw.role,
               COALESCE (
                        ARRAY_AGG(DISTINCT fw.id),
                        '{}'
               ) film_ids
            FROM content.person p
            LEFT JOIN content.person_film_work pfw ON pfw.person_id = p.id
            LEFT JOIN content.film_work fw ON fw.id = pfw.film_work_id
            WHERE pfw.role = %s AND p.modified > %s
            GROUP BY pfw.role, p.id
            ORDER BY p.modified
            OFFSET %s
            """

            self.pg_sc.get_state()

            cur.execute(sql_query, (role,
                                    self.pg_sc.timestamp,
                                    self.pg_sc.state))
            while results := cur.fetchmany(self.page_size):
                yield tuple(Persons(*i)
                            for i in results)
