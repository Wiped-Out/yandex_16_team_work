from providers import mailing
from services.mailing_client import MailJetMailingClient
from mailjet_rest import Client
from core.config import settings


def startup():
    mailing.mailing_client = MailJetMailingClient(
        client=Client(
            auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY),
            version='v3.1',
        )
    )


if __name__ == '__main__':
    startup()
