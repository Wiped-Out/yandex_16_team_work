import uuid
from dataclasses import dataclass, astuple
from datetime import datetime

from pydantic import validate_arguments


# Наследуемый класс для базовых функций
@dataclass
class BaseDataclass:
    # Для реализации распаковки
    def __iter__(self):
        return iter(astuple(self))


@validate_arguments
@dataclass
class Filmwork(BaseDataclass):
    title: str
    description: str
    creation_date: datetime
    created: datetime
    modified: datetime
    type: str
    file_path: str
    rating: float
    id: uuid.UUID


@validate_arguments
@dataclass
class Genre(BaseDataclass):
    name: str
    description: str
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
