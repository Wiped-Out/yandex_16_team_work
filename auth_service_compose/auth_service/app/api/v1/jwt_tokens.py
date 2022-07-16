from http import HTTPStatus

from flask import current_app, Response
from flask_jwt_extended import jwt_required, get_jwt, current_user, get_jti
from flask_restful import Resource, reqparse

from schemas import schemas
from services.jwt import get_jwt_service
from services.user import get_user_service
from utils.utils import log_activity, save_activity


class JWTLogin(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("login", type=str)
        self.parser.add_argument("password", type=str)

    def post(self):
        args = self.parser.parse_args()

        jwt_service = get_jwt_service()
        user_service = get_user_service()

        user = user_service.filter_by(login=args['login'], _first=True)

        if user and user.check_password(args['password']):
            refresh_token = jwt_service.create_refresh_token(user=user)

            token = jwt_service.create_access_token(user=user)

            save_activity(user)

            return Response(
                response=schemas.JWT(access_token=token, refresh_token=refresh_token).json(),
                status=HTTPStatus.OK,
                content_type="application/json")
        else:
            return Response(status=HTTPStatus.BAD_REQUEST)


class JWTLogout(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("refresh_token", type=str)

    @log_activity()
    @jwt_required()
    def post(self):
        args = self.parser.parse_args()

        jwt_service = get_jwt_service()

        token_jti = get_jwt()['jti']
        refresh_token_jti = get_jti(args['refresh_token'])

        jwt_service.block_token(cache_key=token_jti,
                                expire=current_app.config["JWT_ACCESS_TOKEN_EXPIRES"])

        jwt_service.block_token(cache_key=refresh_token_jti,
                                expire=current_app.config["JWT_REFRESH_TOKEN_EXPIRES"])

        return Response(status=HTTPStatus.NO_CONTENT)


class JWTRefresh(Resource):
    @log_activity()
    @jwt_required(refresh=True)
    def post(self):
        jwt_service = get_jwt_service()

        token = jwt_service.create_access_token(user=current_user)

        return Response(
            response=schemas.JWTRefresh(access_token=token).json(),
            status=HTTPStatus.OK,
            content_type="application/json")
