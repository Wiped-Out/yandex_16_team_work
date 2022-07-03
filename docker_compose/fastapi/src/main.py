import aioredis
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles

from api.v1 import films, persons, genres
from core.config import settings
from db import db, cache_db
from services.base_cache import BaseRedisStorage
from services.base_full_text_search import BaseElasticStorage

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    root_path='/fapi',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    cache_db.cache = BaseRedisStorage(redis=await aioredis.create_redis_pool((
        settings.REDIS_HOST, settings.REDIS_PORT
    ), minsize=10, maxsize=20))
    db.full_text_search = BaseElasticStorage(
        elastic=AsyncElasticsearch(hosts=[f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}'])
    )


@app.on_event('shutdown')
async def shutdown():
    cache_db.cache.close()
    await cache_db.cache.wait_closed()
    await db.full_text_search.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8001,
    )
