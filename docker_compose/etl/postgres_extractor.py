from dataclasses import dataclass
from typing import Tuple

from models import ElasticIndexModel
from psycopg2.extensions import connection as _connection
from state_controller import StateController


@dataclass
class PostgresExtractor:
    """Класс для выгрузки данных из PostgreSQL"""
    pgconn: _connection
    pg_sc: StateController
    page_size: int = 500

    def extract(self) -> Tuple[ElasticIndexModel]:
        with self.pgconn.cursor() as cur:
            sql_query = """
            SELECT
               fw.id,
               fw.rating,
               COALESCE (
                        ARRAY_AGG(DISTINCT g.name),
                        '{}'
               ) genre,
               fw.title,
               fw.description,
               COALESCE (
                        ARRAY_AGG(DISTINCT p.full_name)
                        FILTER(WHERE pfw.role = 'director'),
                        '{}'
               ) director,
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
                   JSON_AGG(
                           DISTINCT jsonb_build_object(
                               'id', p.id,
                               'name', p.full_name
                         )
                        ) FILTER(WHERE pfw.role = 'actor'),
                   '[]'
               ) actors,
               COALESCE (
                   JSON_AGG(
                           DISTINCT jsonb_build_object(
                               'id', p.id,
                               'name', p.full_name
                         )
                        ) FILTER(WHERE pfw.role = 'writer'),
                   '[]'
               ) writer
            FROM content.film_work fw
            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
            LEFT JOIN content.person p ON p.id = pfw.person_id
            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
            LEFT JOIN content.genre g ON g.id = gfw.genre_id
            WHERE fw.modified > %s
            GROUP BY fw.id
            ORDER BY fw.modified
            OFFSET %s
            """

            self.pg_sc.get_state()

            cur.execute(sql_query, (self.pg_sc.timestamp, self.pg_sc.state))
            while results := cur.fetchmany(self.page_size):
                yield tuple(ElasticIndexModel(*i)
                            for i in results)
