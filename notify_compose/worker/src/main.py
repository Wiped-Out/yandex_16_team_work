import asyncio
import json

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from core.config import settings
from mailjet_rest import Client
from providers import mailing
from services.mailing_client import MailJetMailingClient


async def on_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        data = json.loads(message.body.decode('utf-8'))


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
        settings.RABBIT_QUEUE_NAME,
        durable=True,
        arguments={'x-max-priority': settings.RABBIT_MAX_PRIORITY}
    )

    await queue.consume(on_message)

    await asyncio.Future()


def startup():
    mailing.mailing_client = MailJetMailingClient(
        client=Client(
            auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY),
            version='v3.1',
        )
    )


if __name__ == '__main__':
    startup()
    asyncio.run(main())
