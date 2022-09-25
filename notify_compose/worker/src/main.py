import argparse
import asyncio
import json

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from mailjet_rest import Client
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings
from db import db
from models.models import (EmailMessage, EmailReceiver, EmailSender,
                           Notification, NotificationTypeEnum, Template,
                           TemplateTypeEnum)
from providers import mailing
from services.data_scrapper import AsyncScrapper
from services.mailing import MailingService
from services.mailing_client import MailJetMailingClient
from services.main_db import BaseMongoStorage
from services.templater import Templater


async def on_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        # get messasge data from RabbitMQ
        data = json.loads(message.body.decode('utf-8'))

        # get notification data from MongoDB
        notification = Notification(**(await db.db.get_one(settings.NOTIFICATIONS_COLLECTION,
                                                           data['notification_id'])))
        template = Template(**(await db.db.find(settings.TEMPLATES_COLLECTION,
                                                template_id=notification.template_id)))
        scrapper = AsyncScrapper(items=template.fields, ready_data={"user_id": data['user_id']})
        ready_data = scrapper.get_result()
        ready_template = Templater.render(template, ready_data)

        scrapper = AsyncScrapper(
            items={
                'name': 'user',
                'url': 'http://nginx_auth:80/api/users/,start,user_id,end,',
                'body': {},
                'headers': {},
                'fetch_result': ""
            },
            ready_data={"user_id": data['user_id']}
        )
        ready_user_data = scrapper.get_result()

        mailer = MailingService()
        mailer.send_email(messages=[
            EmailMessage(
                From=EmailSender(
                    Email=settings.SENDER_EMAIL,
                    Name=settings.SENDER_NAME
                ),
                To=EmailReceiver(
                    Email=ready_user_data['email'],
                    Name=ready_user_data['login']
                ),
                Subject=template.subject,
                TextPart=ready_template if template.template_type is TemplateTypeEnum.plain else "",
                HTMLPart=ready_template if template.template_type is TemplateTypeEnum.html else ""
            )
        ])


async def main() -> None:
    connection = await connect(
        host=settings.RABBIT_HOST,
        port=settings.RABBIT_PORT,
        login=settings.RABBIT_USER,
        password=settings.RABBIT_PASSWORD
    )

    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    queue = await channel.declare_queue(
        args.queue_name.value,
        durable=True,
        arguments={'x-max-priority': settings.RABBIT_MAX_PRIORITY}
    )

    await queue.consume(on_message)

    await asyncio.Future()


def startup():
    MONGODB_URL = f'mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}' \
                  f'@{settings.MONGO_HOST}:{settings.MONGO_PORT}'
    client = AsyncIOMotorClient(MONGODB_URL, uuidRepresentation='standard')
    db.db = BaseMongoStorage(db=client[settings.MONGO_DB_NAME])

    mailing.mailing_client = MailJetMailingClient(
        client=Client(
            auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY),
            version='v3.1',
        )
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Worker')
    parser.add_argument(
        'queue_name',
        type=NotificationTypeEnum,
        choices=list(NotificationTypeEnum),
        help='notification type'
    )
    parser.add_argument(
        'transport',
        type=str,
        help='transport'
    )
    args = parser.parse_args()

    startup()
    asyncio.run(main())
