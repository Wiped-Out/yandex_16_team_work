import logging
from http import HTTPStatus
from logging import config as logging_config
from traceback import format_exception

import aioredis
import uvicorn
from api.v1 import films, genres, persons
from core.config import settings
from core.logger import LOGGING
from db import cache_db, db
from elasticsearch import AsyncElasticsearch
from extensions import logstash, sentry
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from logstash.handler_udp import LogstashHandler
from services.base_cache import BaseRedisStorage
from services.base_full_text_search import BaseElasticStorage


def init_logstash():
    if not settings.ENABLE_LOGSTASH:
        return
    logstash.logstash_handler = LogstashHandler(settings.LOGSTASH_HOST,
                                                settings.LOGSTASH_PORT,
                                                version=1)
    logstash.logstash_handler.addFilter(logstash.RequestIdFilter())


def init_logger(app: FastAPI):
    logging_config.dictConfig(LOGGING)
    app.logger = logging.getLogger(__name__)  # type: ignore
    app.logger.setLevel(logging.INFO)  # type: ignore

    if settings.ENABLE_LOGSTASH:
        app.logger.addHandler(logstash.logstash_handler)  # type: ignore


def init_app() -> FastAPI:
    sentry.init_sentry()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url='/api/openapi',
        openapi_url='/api/openapi.json',
        root_path='/fapi',
        default_response_class=ORJSONResponse,
    )

    init_logstash()
    init_logger(app=app)
    return app


app = init_app()


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    log_str = f'Error catched \n {format_exception(type(exc), exc, exc.__traceback__)}'

    app.logger.info(log_str, {'request_id': request.headers.get('X-Request-Id')})  # type: ignore
    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST, detail='Bad request',
    )


@app.on_event('startup')
async def startup():
    cache_db.cache = BaseRedisStorage(redis=await aioredis.create_redis_pool((
        settings.REDIS_HOST, settings.REDIS_PORT,
    ), minsize=10, maxsize=20))

    db.full_text_search = BaseElasticStorage(
        elastic=AsyncElasticsearch(hosts=[f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}']),
    )


@app.on_event('shutdown')
async def shutdown():
    await cache_db.cache.close()
    await db.full_text_search.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])

app.mount('/static', StaticFiles(directory='static'), name='static')

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8001,
    )
