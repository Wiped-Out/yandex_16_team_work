from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Optional

from authlib.integrations.flask_client import OAuth
from flask import url_for

from extensions.oauth import get_oauth, get_google_client
from extensions.tracer import _trace


class OauthServiceClient(ABC):

    @abstractmethod
    def get_client(self, **kwargs):
        pass

    @abstractmethod
    def register_redirect(self, **kwargs):
        pass

    @abstractmethod
    def login_redirect(self, **kwargs):
        pass

    @abstractmethod
    def get_user_data_from_token(self, **kwargs):
        pass


class GoogleOauthServiceClient(OauthServiceClient):
    @_trace()
    def get_client(self, oauth: Optional[OAuth] = None, **kwargs):
        return get_google_client()

    @_trace()
    def register_redirect(self, **kwargs):
        client = self.get_client()
        redirect_uri = url_for('oauth.oauth_register', provider='google', _external=True)
        return client.authorize_redirect(redirect_uri)

    @_trace()
    def login_redirect(self, **kwargs):
        client = self.get_client()
        redirect_uri = url_for('oauth.oauth_login', provider='google', _external=True)
        return client.authorize_redirect(redirect_uri)

    @_trace()
    def get_user_data_from_token(self, **kwargs):
        oauth = get_oauth()
        client = self.get_client(oauth=oauth)
        token = client.authorize_access_token()
        resp = client.get('userinfo')
        user_info = resp.json()
        user = oauth.google.userinfo()
        sub, email, username = user['sub'], user['email'], user['email'].split('@')[0]
        return sub, email, username


@lru_cache()
def get_google_oauth_client_service(
) -> GoogleOauthServiceClient:
    return GoogleOauthServiceClient()
