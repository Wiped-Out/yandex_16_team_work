import logging
from http import HTTPStatus
from logging import config as logging_config
from traceback import format_exception

import uvicorn
from api.v1 import notifications, templates
from core.config import settings
from core.logger import LOGGING
from db import db
from extensions import logstash, sentry
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from logstash.handler_udp import LogstashHandler
from motor.motor_asyncio import AsyncIOMotorClient
from services.main_db import BaseMongoStorage

from fastapi import FastAPI, HTTPException, Request


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


@app.on_event('startup')
async def startup():
    MONGODB_URL = f'mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}' \
                  f'@{settings.MONGO_HOST}:{settings.MONGO_PORT}'
    client = AsyncIOMotorClient(MONGODB_URL, uuidRepresentation='standard')
    db.db = BaseMongoStorage(db=client[settings.MONGO_DB_NAME])


@app.on_event('shutdown')
async def shutdown():
    pass


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    log_str = f'Error catched \n {format_exception(type(exc), exc, exc.__traceback__)}'

    app.logger.info(log_str, {'request_id': request.headers.get('X-Request-Id')})  # type: ignore
    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST, detail='Bad request',
    )


app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(templates.router, prefix='/api/v1/templates', tags=['templates'])
app.include_router(notifications.router, prefix='/api/v1/notifications', tags=['notifications'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8001,
    )
