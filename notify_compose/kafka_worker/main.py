import asyncio

from kafka import KafkaConsumer, KafkaProducer

from core.config import settings
from core.notify_templates import topics_to_notify_template
from db import db
from services.db import BaseKafkaStorage, MainStorage
from services.event_handler import EventService


async def startup():
    db.db = BaseKafkaStorage(db_producer=KafkaProducer(
        bootstrap_servers=[f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}'],
        api_version=(0, 11, 5),
    ),
        db_consumer=KafkaConsumer(
            bootstrap_servers=[f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}'],
            api_version=(0, 11, 5),
        ))


async def main():
    await startup()

    kafka_service = MainStorage(db=db.db)
    event_handler_service = EventService()
    try:
        await kafka_service.subscribe(topics=settings.TOPICS_NAMES)
        print(settings.TOPICS_NAMES, flush=True)
        for message in await kafka_service.consume():
            print(message, flush=True)
            template = topics_to_notify_template[message.topic]
            await event_handler_service.handle_event(data_from_topic=message.value,
                                                     notification_template=template)
    finally:
        await kafka_service.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
