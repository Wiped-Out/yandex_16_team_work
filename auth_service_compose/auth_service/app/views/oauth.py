import werkzeug.exceptions
from flask import Blueprint, make_response, redirect
from flask_jwt_extended import set_access_cookies, set_refresh_cookies

from core.settings import settings
from extensions.tracer import _trace
from models.models import ActionsEnum, OAuthEnum
from services.jwt import get_jwt_service
from services.oauth import get_oauth_service
from services.oauth_client import get_google_oauth_client_service
from services.user import get_user_service
from utils.utils import save_activity, generate_password

oauth_view = Blueprint('oauth', __name__, template_folder='templates')


@oauth_view.route(settings.GOOGLE_OAUTH_URL_REGISTER, methods=['GET'])
@_trace()
def google_oauth_register():
    google_oauth_service = get_google_oauth_client_service()
    user_data = google_oauth_service.get_user_data_from_token()

    jwt_service = get_jwt_service()
    user_service = get_user_service()
    oauth_service = get_oauth_service()

    login = user_data['email'].split('@')[0]

    if user_service.filter_by(login=login, _first=True) or \
            user_service.filter_by(email=user_data['email'], _first=True):
        return make_response(redirect('/login'))

    user = user_service.create_user(params={"login": login,
                                            "email": user_data['email'],
                                            "password": generate_password()})
    oauth_service.create_oauth(params={
        "user_id": user.id,
        "type": OAuthEnum.google,
        "sub": user_data['sub']
    })

    response = make_response(redirect('/happy'))

    refresh_token = jwt_service.create_refresh_token(user=user)

    token = jwt_service.create_access_token(user=user)

    set_access_cookies(response, token)
    set_refresh_cookies(response, refresh_token)

    save_activity(user, action=ActionsEnum.login)
    return response


@oauth_view.route(settings.GOOGLE_OAUTH_URL_REGISTER_REDIRECT, methods=['GET'])
@_trace()
def google_oauth_register_redir():
    google_oauth_service = get_google_oauth_client_service()
    return google_oauth_service.register_redirect()


@oauth_view.route(settings.GOOGLE_OAUTH_URL_LOGIN, methods=['GET'])
@_trace()
def google_oauth_login():
    google_oauth_service = get_google_oauth_client_service()
    user_data = google_oauth_service.get_user_data_from_token()

    if not user_data:
        return make_response(redirect("/register"))

    jwt_service = get_jwt_service()
    user_service = get_user_service()
    oauth_service = get_oauth_service()

    oauth = oauth_service.get_oauth(sub=user_data['sub'], type=OAuthEnum.google)

    if not oauth:
        return make_response(redirect("/register"))

    user = user_service.get(item_id=oauth.user_id)

    response = make_response(redirect('/happy'))

    refresh_token = jwt_service.create_refresh_token(user=user)

    token = jwt_service.create_access_token(user=user)

    set_access_cookies(response, token)
    set_refresh_cookies(response, refresh_token)

    save_activity(user, action=ActionsEnum.login)
    return response


@oauth_view.route(settings.GOOGLE_OAUTH_URL_LOGIN_REDIRECT, methods=['GET'])
@_trace()
def google_oauth_login_redir():
    google_oauth_service = get_google_oauth_client_service()
    return google_oauth_service.login_redirect()
