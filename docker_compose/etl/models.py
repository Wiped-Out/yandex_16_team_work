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
class ElasticIndexModel(BaseDataclass):
    id: uuid.UUID
    imdb_rating: Union[float, None]
    genre: List[str]
    title: str
    description: Union[str, None]
    director: List[str]
    actors_names: List[str]
    writers_names: List[str]
    actors: List[Dict]
    writers: List[Dict]
