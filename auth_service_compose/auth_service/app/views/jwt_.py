from flask import Blueprint, redirect, current_app, request, make_response
from flask_jwt_extended import jwt_required, get_jti, unset_jwt_cookies

from services.jwt import get_jwt_service
from services.refresh_token import get_refresh_token_service
from utils.utils import log_activity

jwt__view = Blueprint('jwt_', __name__, template_folder='templates')


@jwt__view.route('/logout', methods=['GET'])
@jwt_required()
@log_activity()
def logout():
    jwt_service = get_jwt_service()
    refresh_token_service = get_refresh_token_service()

    token = request.cookies.get(key=current_app.config["JWT_ACCESS_COOKIE_NAME"])
    refresh_token = request.cookies.get(key=current_app.config["JWT_REFRESH_COOKIE_NAME"])

    token_jti = get_jti(token)
    refresh_token_jti = get_jti(refresh_token)

    jwt_service.block_token(cache_key=token_jti,
                            expire=current_app.config["JWT_ACCESS_TOKEN_EXPIRES"])

    token_id = refresh_token_service.filter(token=refresh_token, _first=True).id
    refresh_token_service.delete(item_id=token_id)
    jwt_service.block_token(cache_key=refresh_token_jti,
                            expire=current_app.config["JWT_REFRESH_TOKEN_EXPIRES"])

    response = make_response(redirect('/'))
    unset_jwt_cookies(response)

    return response
