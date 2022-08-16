import random
import time

from faker import Faker
from faker.providers.lorem.ru_RU import Provider as lorem
from kafka import KafkaProducer
from loguru import logger
from pydantic import UUID4

from config import settings
from models import FilmBookmark, FilmLike, FilmProgress, UserComment

fake = Faker()
Faker.seed(4321)

# Generate films
films = [fake.uuid4() for _ in range(settings.MAX_NUMBER_FILMS)]
users = []


def gen_film_like(user_id: UUID4) -> tuple:
    film_id = random.choice(films)
    film_like = FilmLike(user_id=user_id, film_id=film_id)
    return film_like.json().encode(), f"{user_id}+{film_id}".encode()


def gen_film_bookmark(user_id: UUID4) -> tuple:
    film_id = random.choice(films)
    film_bookmark = FilmBookmark(user_id=user_id, film_id=film_id)
    return film_bookmark.json().encode(), f"{user_id}+{film_id}".encode()


def gen_film_progress(user_id: UUID4) -> tuple:
    film_id = random.choice(films)
    # Average runtime ~ 1 h 40 m = 100 m = 6000 s
    timestamp = random.randint(0, 6000)
    film_progress = FilmProgress(
        user_id=user_id, film_id=film_id, timestamp=timestamp)
    return film_progress.json().encode(), f"{user_id}+{film_id}".encode()


def gen_user_comment(user_id: UUID4) -> tuple:
    film_id = random.choice(films)
    fake.add_provider(lorem)
    comment = fake.paragraph(nb_sentences=2)
    created_at = fake.date_time_between(start_date="-2y")
    user_comment = UserComment(
        user_id=user_id, film_id=film_id, comment=comment, created_at=created_at)
    return user_comment.json().encode(), f"{user_id}+{film_id}".encode()


def produce_msgs(producer: KafkaProducer) -> None:
    i = 0
    while i < settings.MAX_NUMBER_USERS:
        user_id = fake.uuid4()
        users.append(user_id)

        # Likes
        for _ in range(random.randint(0, 20)):
            message, key = gen_film_like(user_id)
            # producer.send(topic="film_likes", value=message, key=key)
            try:
                producer.send(topic="film_likes", value=message, key=key)
            except Exception as e:
                logger.error(e)

        # Bookmarks
        for _ in range(random.randint(0, 20)):
            message, key = gen_film_bookmark(user_id)
            try:
                producer.send(topic="film_bookmarks", value=message, key=key)
            except Exception as e:
                logger.error(e)

        # Progress
        for _ in range(random.randint(0, 30)):
            message, key = gen_film_progress(user_id)
            try:
                producer.send(topic="film_progress", value=message, key=key)
            except Exception as e:
                logger.error(e)

        # Comments
        for _ in range(random.randint(0, 10)):
            message, key = gen_user_comment(user_id)
            try:
                producer.send(topic="user_comments", value=message, key=key)
            except Exception as e:
                logger.error(e)

        # Sleeping time
        sleep_time = random.randint(
            0, int(settings.MAX_WAITING_TIME * 10000)) / 10000
        logger.info("Sleeping for..." + str(sleep_time) + "s")
        time.sleep(sleep_time)

        # Force flushing of all messages
        if (i % 100) == 0:
            producer.flush()

        i = i + 1

    producer.flush()


def main():
    producer = KafkaProducer(
        bootstrap_servers=[settings.KAFKA_HOSTNAME +
                           ":" + settings.KAFKA_PORT])
    logger.info(f"Bootstrap is connected: {producer.bootstrap_connected()}")
    produce_msgs(producer)


if __name__ == "__main__":
    main()
