from typing import Optional

from core.settings import settings
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from services.base_main import BaseSQLAlchemyStorage, MainStorage

db: Optional[MainStorage] = None
sqlalchemy = SQLAlchemy()


def init_sqlalchemy(app: Flask, storage: BaseSQLAlchemyStorage):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}?options=-c%20search_path=content'  # noqa: E501
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    storage.db.init_app(app)


def get_db() -> MainStorage:
    if not db:
        raise
    return db
