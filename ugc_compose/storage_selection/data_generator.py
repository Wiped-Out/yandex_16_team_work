import json
import random

from config import settings
from faker import Faker
from faker.providers.lorem.ru_RU import Provider as lorem
from models import FilmBookmark, FilmLike, UserReview

fake = Faker()
Faker.seed(4321)


class DataGenerator():
    def __init__(self):
        self.films = [str(fake.uuid4())
                      for _ in range(settings.MAX_NUMBER_FILMS)]
        self.users = []
        self.likes = []
        self.bookmarks = []
        self.reviews = []

    def gen_film_like(self, user_id: str) -> FilmLike:
        film_id = random.choice(self.films)
        rating = random.randint(1, 10)
        return FilmLike(user_id=user_id, film_id=film_id, rating=rating)

    def gen_film_bookmark(self, user_id: str) -> FilmBookmark:
        film_id = random.choice(self.films)
        return FilmBookmark(user_id=user_id, film_id=film_id)

    def gen_user_review(self, user_id: str) -> UserReview:
        film_id = random.choice(self.films)
        fake.add_provider(lorem)
        text = fake.paragraph(nb_sentences=2)
        created_at = fake.date_time_between(start_date="-2y")
        return UserReview(
            user_id=user_id, film_id=film_id, text=text, created_at=created_at)


if __name__ == '__main__':
    data_generator = DataGenerator()
    i = 0

    films_file = open('data/films.json', 'w')
    users_file = open('data/users.json', 'w')
    likes_file = open('data/likes.json', 'w')
    bookmarks_file = open('data/bookmarks.json', 'w')
    reviews_file = open('data/reviews.json', 'w', encoding='utf-8')

    while i < settings.MAX_NUMBER_USERS:
        user_id = str(fake.uuid4())
        data_generator.users.append(user_id)

        # Likes
        for _ in range(random.randint(0, 20)):
            data_generator.likes.append(
                data_generator.gen_film_like(user_id).dict())

        # Bookmarks
        for _ in range(random.randint(0, 20)):
            data_generator.bookmarks.append(
                data_generator.gen_film_bookmark(user_id).dict())

        # Reviews
        for _ in range(random.randint(0, 10)):
            data_generator.reviews.append(
                data_generator.gen_user_review(user_id).dict())

        i = i + 1

    json.dump(data_generator.films, films_file, indent=4)
    json.dump(data_generator.users, users_file, indent=4)
    json.dump(data_generator.likes, likes_file, indent=4)
    json.dump(data_generator.bookmarks, bookmarks_file,
              indent=4)
    json.dump(data_generator.reviews, reviews_file,
              indent=4, default=str, ensure_ascii=False)

    films_file.close()
    users_file.close()
    likes_file.close()
    bookmarks_file.close()
    reviews_file.close()
