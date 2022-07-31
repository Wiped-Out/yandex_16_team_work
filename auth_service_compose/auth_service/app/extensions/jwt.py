from datetime import datetime, timezone
from http import HTTPStatus
from typing import Optional

from flask import request, redirect, current_app, make_response
from flask_jwt_extended import JWTManager, set_access_cookies, unset_jwt_cookies, get_jti
from flask_restx import reqparse
from jwt.exceptions import InvalidTokenError

from services.jwt import get_jwt_service
from services.user import get_user_service
from utils.utils import make_error_response, work_in_context

jwt_manager: Optional[JWTManager] = None

jwt_parser = reqparse.RequestParser()
jwt_parser.add_argument('Authorization', location="headers")


def set_jwt_callbacks():
    @jwt_manager.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]
        jwt_service = get_jwt_service()
        token_in_redis = jwt_service.get_blocked_token(cache_key=jti)
        return token_in_redis is not None

    @jwt_manager.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        if 'api' not in request.url:
            try:
                response = make_response(
                    redirect(request.url_root)
                )

                jwt_service = get_jwt_service()
                user_service = get_user_service()

                refresh_token = request.cookies.get(key=current_app.config["JWT_REFRESH_COOKIE_NAME"])

                get_jti(refresh_token)

                exp_timestamp = jwt_payload["exp"]
                now = datetime.now(timezone.utc)
                target_timestamp = datetime.timestamp(now +
                                                      current_app.config["JWT_ACCESS_TOKEN_EXPIRES"])

                if target_timestamp > exp_timestamp:
                    access_token = jwt_service.create_access_token(user=user_service.get(
                        item_id=jwt_payload['sub']))

                    set_access_cookies(response, access_token)

                return response

            except (RuntimeError, KeyError, InvalidTokenError, AttributeError):
                response = make_response(redirect('/login'))

                unset_jwt_cookies(response)

                return response

        return make_error_response(msg="Token has expired",
                                   status=HTTPStatus.UNAUTHORIZED)

    @jwt_manager.token_verification_failed_loader
    def token_verification_failed_loader_callback(_jwt_header, jwt_data):
        if 'api' not in request.url:
            return make_response(redirect('/index'))
        return make_error_response(msg="Invalid JWT token",
                                   status=HTTPStatus.FORBIDDEN)

    @jwt_manager.unauthorized_loader
    def unauthorized_loader_callback(explain):
        if 'api' not in request.url:
            return make_response(redirect('/index'))
        return make_error_response(msg=explain,
                                   status=HTTPStatus.UNAUTHORIZED)

    @jwt_manager.invalid_token_loader
    def invalid_token_loader_callback(explain):
        if 'api' not in request.url:
            return make_response(redirect('/index'))
        return make_error_response(msg=explain,
                                   status=HTTPStatus.FORBIDDEN)

    @jwt_manager.user_identity_loader
    @work_in_context(current_app)
    def user_identity_lookup(user):
        return user.id

    @jwt_manager.user_lookup_loader
    @work_in_context(current_app)
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        user_service = get_user_service()
        return user_service.get(item_id=identity)


def get_jwt_manager() -> JWTManager:
    return jwt_manager
