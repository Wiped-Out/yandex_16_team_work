import datetime
import logging
import os
import time

import psycopg2
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch_db import ElasticSearchManager
from elasticsearch_loader import ElasticsearchLoader
from postgres_extractor import PostgresExtractor
from postgresql_db import PostgreSQLManager
from psycopg2.extensions import connection as _connection
from pydantic import BaseSettings
from state_controller import StateController

load_dotenv()


class PostgresDSL(BaseSettings):
    dbname: str = os.environ.get('DB_NAME')
    user: str = os.environ.get('DB_USER')
    password: str = os.environ.get('DB_PASSWORD')
    host: str = os.environ.get('DB_HOST', '127.0.0.1')
    port: int = os.environ.get('DB_PORT', 5432)


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
    postgres_extractor = PostgresExtractor(pgconn,
                                           pg_sc,
                                           PG_PAGE_SIZE)
    es_sc = StateController('elasticsearch.state')
    elasticsearch_loader = ElasticsearchLoader(esconn,
                                               es_sc,
                                               ELASTIC_PAGE_SIZE)
    for data in postgres_extractor.extract():
        elasticsearch_loader.load(data)

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
    dsl = PostgresDSL().dict()
    while True:
        is_successful = False
        while not is_successful:
            try:
                with PostgreSQLManager(dsl) as pg_conn, \
                        ElasticSearchManager(
                            os.environ.get('ELASTIC_URI')
                        ) as es_conn:
                    is_successful = load_data(pg_conn, es_conn)
            except ConnectionError:
                pass
        time.sleep(600)
