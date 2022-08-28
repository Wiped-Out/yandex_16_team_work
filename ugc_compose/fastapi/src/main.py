import uvicorn
from api.v1 import bookmarks, comments, film_progress, likes
from core.config import settings
from db import db
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from kafka import KafkaProducer
from services.main_db import BaseKafkaStorage

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    root_path='/fapi',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    db.db = BaseKafkaStorage(
        db=KafkaProducer(
            bootstrap_servers=[f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}'],
            api_version=(0, 11, 5),
        ),
    )


@app.on_event('shutdown')
async def shutdown():
    pass


app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(comments.router, prefix='/api/v1/comments', tags=['comments'])
app.include_router(bookmarks.router, prefix='/api/v1/bookmarks', tags=['bookmarks'])
app.include_router(likes.router, prefix='/api/v1/likes', tags=['likes'])
app.include_router(film_progress.router, prefix='/api/v1/film_progress', tags=['film_progress'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8001,
    )
