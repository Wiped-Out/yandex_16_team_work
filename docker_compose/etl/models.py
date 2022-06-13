import uuid
from dataclasses import dataclass, astuple
from typing import Union, List, Dict

from pydantic import validate_arguments


# Наследуемый класс для базовых функций
@dataclass
class BaseDataclass:
    # Для реализации распаковки
    def __iter__(self):
        return iter(astuple(self))


@validate_arguments
@dataclass
class Movies(BaseDataclass):
    id: uuid.UUID
    imdb_rating: Union[float, None]
    genre: List[Dict]
    title: str
    description: Union[str, None]
    directors: List[Dict]
    actors_names: List[str]
    writers_names: List[str]
    directors_names: List[str]
    actors: List[Dict]
    writers: List[Dict]

@validate_arguments
@dataclass
class Persons(BaseDataclass):
    id: uuid.UUID
    full_name: str
    role: str
    film_ids: List[uuid.UUID]