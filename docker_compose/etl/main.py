import datetime
import logging
import time

import psycopg2 as psycopg2
from core.config import postgres_dsl, settings
from elasticsearch import Elasticsearch
from elasticsearch_db import ElasticSearchManager
from elasticsearch_loader import ElasticsearchLoader
from postgres_extractor import PostgresExtractor
from postgresql_db import PostgreSQLManager
from psycopg2.extensions import connection as _connection
from state_controller import StateController

# Для выгрузки/загрузки данных по n записей
PG_PAGE_SIZE = 100
ELASTIC_PAGE_SIZE = 100
START_TIMESTAMP = datetime.datetime.now()
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename='etl.log',
                    encoding='utf-8',
                    level=logging.DEBUG)


def load_data(pgconn: _connection, esconn: Elasticsearch) -> bool:
    """Основной метод загрузки данных из PostgeSQL в Elasticsearch"""
    pg_sc = StateController('postgres.state')
    postgres_extractor = PostgresExtractor(
        pgconn, pg_sc, PG_PAGE_SIZE,
    )

    es_sc = StateController('elasticsearch.state')
    elasticsearch_loader = ElasticsearchLoader(
        esconn, es_sc, ELASTIC_PAGE_SIZE,
    )

    indexes = ('movies',
               'persons',
               'genres',
               )

    methods_args = (
        ('extract_movies', ()),
        ('extract_persons', ()),
        ('extract_genres', ()),
    )

    state_files = (
        ('pg_movies.state', 'es_movies.state'),
        ('pg_persons.state', 'es_persons.state'),
        ('pg_genres.state', 'es_genres.state'),
    )

    for index, files, method_args in zip(indexes, state_files, methods_args):
        pg_sc.file_path, es_sc.file_path = files
        method, args = method_args
        extract_method = getattr(postgres_extractor,
                                 method)

        for data in extract_method(*args):
            elasticsearch_loader.load(index, data)

            pg_sc.get_state()
            pg_sc.state += PG_PAGE_SIZE
            pg_sc.set_state()

            es_sc.state = 0
            es_sc.set_state()
        pg_sc.state = 0
        pg_sc.timestamp = START_TIMESTAMP
        pg_sc.set_state()
    return True


if __name__ == '__main__':
    psycopg2.extras.register_uuid()
    while True:
        is_successful = False
        while not is_successful:
            try:
                with PostgreSQLManager(
                        postgres_dsl.dict(),
                ) as pg_conn, ElasticSearchManager(
                    settings.ELASTIC_URI,
                ) as es_conn:
                    is_successful = load_data(pg_conn, es_conn)
            except ConnectionError:
                pass
        time.sleep(600)
