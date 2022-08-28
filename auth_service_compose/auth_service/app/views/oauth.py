from extensions.tracer import _trace
from flask import Blueprint, make_response, redirect
from models.models import ActionsEnum, OAuthEnum
from services import oauth_client
from services.jwt import get_jwt_service
from services.oauth import get_oauth_service
from services.user import get_user_service
from utils.utils import generate_password, save_activity

oauth_view = Blueprint('oauth', __name__, template_folder='templates')


@oauth_view.route('/oauth2/<provider>/register/callback', methods=['GET'])
@_trace()
def oauth_register(provider):
    oauth_service = getattr(oauth_client, f'get_{provider}_oauth_client_service', None)
    if oauth_service is None:
        return make_response(redirect('/register'))
    oauth_service = oauth_service()
    try:
        sub, email, login = oauth_service.get_user_data_from_token()
    except Exception:
        return make_response(redirect('/register'))

    jwt_service = get_jwt_service()
    user_service = get_user_service()
    oauth_service = get_oauth_service()

    if user_service.filter_by(
            login=login, _first=True,
    ) or user_service.filter_by(
        email=email, _first=True,
    ):
        return make_response(redirect('/login'))

    user = user_service.create_user(params={'login': login,
                                            'email': email,
                                            'password': generate_password()})
    oauth_service.create_oauth(params={
        'user_id': user.id,
        'type': getattr(OAuthEnum, provider),
        'sub': sub,
    })

    response = make_response(redirect('/happy'))

    response = jwt_service.authorize(response=response, user=user)

    save_activity(user, action=ActionsEnum.login)
    return response


@oauth_view.route('/oauth2/<provider>/register', methods=['GET'])
@_trace()
def oauth_register_redir(provider):
    oauth_service = getattr(oauth_client, f'get_{provider}_oauth_client_service', None)
    if oauth_service is None:
        return make_response(redirect('/register'))
    oauth_service = oauth_service()
    return oauth_service.register_redirect()


@oauth_view.route('/oauth2/<provider>/login/callback', methods=['GET'])
@_trace()
def oauth_login(provider):
    oauth_service = getattr(oauth_client, f'get_{provider}_oauth_client_service', None)
    if oauth_service is None:
        return make_response(redirect('/login'))
    oauth_service = oauth_service()
    try:
        sub, email, login = oauth_service.get_user_data_from_token()
    except Exception:
        return make_response(redirect('/login'))

    jwt_service = get_jwt_service()
    user_service = get_user_service()
    oauth_service = get_oauth_service()

    oauth = oauth_service.get_oauth(sub=sub, type=getattr(OAuthEnum, provider))

    if not oauth:
        return make_response(redirect('/register'))

    user = user_service.get(item_id=oauth.user_id)

    response = make_response(redirect('/happy'))

    response = jwt_service.authorize(response=response, user=user)

    save_activity(user, action=ActionsEnum.login)
    return response


@oauth_view.route('/oauth2/<provider>/login', methods=['GET'])
@_trace()
def oauth_login_redir(provider):
    oauth_service = getattr(oauth_client, f'get_{provider}_oauth_client_service', None)
    if oauth_service is None:
        return make_response(redirect('/login'))
    oauth_service = oauth_service()
    return oauth_service.login_redirect()
