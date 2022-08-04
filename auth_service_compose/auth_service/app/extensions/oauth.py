from typing import Optional

from authlib.integrations.flask_client import OAuth
from flask import Flask
from werkzeug.local import LocalProxy

from core.settings import settings

oauth: Optional[OAuth] = OAuth()
google: Optional[LocalProxy] = None


def init_oauth(app: Flask):
    oauth.init_app(app)
    global google
    google = oauth.register(
        name='google',
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
        jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
        # This is only needed if using openId to fetch user info
        client_kwargs={'scope': 'openid email profile'},
    )


def get_oauth() -> OAuth:
    return oauth


def get_google_client() -> LocalProxy:
    return google
