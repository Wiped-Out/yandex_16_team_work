import uuid
from dataclasses import dataclass, astuple
from datetime import datetime
from typing import Union

from pydantic import validate_arguments


# Наследуемый класс для базовых функций
@dataclass
class BaseDataclass:
    # Для реализации распаковки
    def __iter__(self):
        return iter(astuple(self))


# Автоматическая валидация передаваемых параметров
# pydantic.BaseModel не принимает позиционные аргументы,
# dataclass принимает оба варианта аргументов
# распечатка работает парами (ключ, значение) в pydantic.BaseModel,
# можно её переделать, но есть ли смысл тогда менять на pydantic.BaseModel?
@validate_arguments
@dataclass
class Filmwork(BaseDataclass):
    title: str
    description: Union[str, None]
    creation_date: Union[datetime, None]
    created: Union[datetime, None]
    modified: Union[datetime, None]
    type: str
    file_path: Union[str, None]
    rating: Union[float, None]
    id: uuid.UUID


@validate_arguments
@dataclass
class Genre(BaseDataclass):
    name: str
    description: Union[str, None]
    created: datetime
    modified: datetime
    id: uuid.UUID


@validate_arguments
@dataclass
class Person(BaseDataclass):
    full_name: str
    created: datetime
    modified: datetime
    id: uuid.UUID


@validate_arguments
@dataclass
class PersonFilmwork(BaseDataclass):
    role: str
    created: datetime
    id: uuid.UUID
    film_work_id: uuid.UUID
    person_id: uuid.UUID


@validate_arguments
@dataclass
class GenreFilmwork(BaseDataclass):
    created: datetime
    id: uuid.UUID
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
