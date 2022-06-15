import random
import uuid
from dataclasses import dataclass, field
from typing import Tuple, Union, Set

from faker import Faker

from models import Filmwork, Person, Genre, GenreFilmwork, PersonFilmwork


@dataclass
class DataFaker:
    """Класс для создания фейковых данных"""
    page_size: int = 500
    filmworks_amount: int = 200_000
    genres_amount: int = 120
    persons_amount: int = 100_000
    filmworks_ids: Union[Set[uuid.uuid4], Tuple[uuid.uuid4]] \
        = field(default_factory=set)
    genres_ids: Union[Set[uuid.uuid4], Tuple[uuid.uuid4]] \
        = field(default_factory=set)
    persons_ids: Union[Set[uuid.uuid4], Tuple[uuid.uuid4]] \
        = field(default_factory=set)

    def get_filmworks(self) -> Tuple[Filmwork]:
        faker = Faker()
        ready_data = []

        for _ in range(self.filmworks_amount):
            data = {
                'title': faker.unique.sentence(),
                'description': faker.unique.paragraph(nb_sentences=4),
                'creation_date': faker.unique.date_time(),
                'created': faker.unique.date_time_this_century(),
                'modified': faker.unique.date_time_this_century(),
                'type': random.choice(('movie', 'tv_show')),
                'file_path': '',
                'rating': round(random.uniform(0, 10), 1),
                'id': uuid.uuid4()
            }
            ready_data.append(Filmwork(**data))
            self.filmworks_ids.add(data['id'])

            if len(ready_data) == self.page_size:
                yield tuple(ready_data)
                ready_data = []

        if ready_data:
            yield tuple(ready_data)

    def get_genres(self) -> Tuple[Genre]:
        faker = Faker()
        ready_data = []

        for _ in range(self.genres_amount):
            data = {
                'name': faker.unique.word(),
                'description': faker.unique.paragraph(nb_sentences=3),
                'created': faker.unique.date_time_this_century(),
                'modified': faker.unique.date_time_this_century(),
                'id': uuid.uuid4()
            }
            ready_data.append(Genre(**data))
            self.genres_ids.add(data['id'])

            if len(ready_data) == self.page_size:
                yield tuple(ready_data)
                ready_data = []

        if ready_data:
            yield tuple(ready_data)

    def get_persons(self) -> Tuple[Person]:
        faker = Faker()
        ready_data = []

        for _ in range(self.persons_amount):
            data = {
                'full_name': faker.unique.name(),
                'created': faker.unique.date_time_this_century(),
                'modified': faker.unique.date_time_this_century(),
                'id': uuid.uuid4()
            }
            ready_data.append(Person(**data))
            self.persons_ids.add(data['id'])

            if len(ready_data) == self.page_size:
                yield tuple(ready_data)
                ready_data = []

        if ready_data:
            yield tuple(ready_data)

    def get_genres_filmworks(self) -> Tuple[GenreFilmwork]:
        self.filmworks_ids = tuple(self.filmworks_ids)
        self.genres_ids = tuple(self.genres_ids)

        faker = Faker()

        ready_data = []
        n = 0

        for i in range(len(self.filmworks_ids)):
            data = {
                'created': faker.unique.date_time_this_century(),
                'id': uuid.uuid4(),
                'film_work_id': self.filmworks_ids[i],
                'genre_id': self.genres_ids[n % self.genres_amount]
            }
            n += 1
            ready_data.append(GenreFilmwork(**data))

            if len(ready_data) == self.page_size:
                yield tuple(ready_data)
                ready_data = []

        if ready_data:
            yield tuple(ready_data)

    def get_persons_filmworks(self) -> Tuple[PersonFilmwork]:
        self.filmworks_ids = tuple(self.filmworks_ids)
        self.persons_ids = tuple(self.persons_ids)

        ready_data = []
        n = 0
        crew = ('actor', 'director', 'writer')
        faker = Faker()
        for i in range(len(self.filmworks_ids)):

            for j in range(len(crew)):
                data = {
                    'role': crew[j],
                    'created': faker.unique.date_time_this_century(),
                    'id': uuid.uuid4(),
                    'film_work_id': self.filmworks_ids[i],
                    'person_id': self.persons_ids[n % self.persons_amount]
                }
                n += 1
                ready_data.append(PersonFilmwork(**data))

                if len(ready_data) == self.page_size:
                    yield tuple(ready_data)
                    ready_data = []

        if ready_data:
            yield tuple(ready_data)
