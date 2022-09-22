from http import HTTPStatus

from api.v1.__base__ import base_url
from extensions.jwt import jwt_parser
from flask import Response, current_app
from flask_jwt_extended import current_user, get_jti, get_jwt, jwt_required
from flask_restx import Namespace, Resource, fields, reqparse
from models.models import ActionsEnum
from schemas.v1 import responses, schemas
from services.jwt import get_jwt_service
from services.refresh_token import get_refresh_token_service
from services.user import get_user_service
from utils.utils import log_activity, make_error_response, save_activity

jwt_tokens = Namespace('JWT', path=f'{base_url}/', description='')

JWT = jwt_tokens.model('JWT',
                       {
                           'access_token': fields.String,
                           'refresh_token': fields.String,
                       },
                       )

_JWTRefresh = jwt_tokens.model('JWTRefresh',
                               {
                                   'access_token': fields.String,
                               },
                               )

login_parser = reqparse.RequestParser()
login_parser.add_argument('login', type=str, location='json')
login_parser.add_argument('password', type=str, location='json')

logout_parser = reqparse.RequestParser()
logout_parser.add_argument('refresh_token', type=str, location='json')

logout_everywhere = reqparse.RequestParser()
logout_everywhere.add_argument('password', type=str, location='json')


@jwt_tokens.route('/login')
class JWTLogin(Resource):

    @jwt_tokens.response(code=int(HTTPStatus.OK), description=' ', model=JWT)
    @jwt_tokens.response(code=int(HTTPStatus.BAD_REQUEST), description=' ')
    @jwt_tokens.expect(login_parser)
    def post(self):
        args = login_parser.parse_args()

        jwt_service = get_jwt_service()
        user_service = get_user_service()

        user = user_service.filter_by(login=args['login'], _first=True)

        if not (user and user.check_password(args['password'])):
            return make_error_response(
                msg=responses.PROBLEMS_WITH_USER,
                status=HTTPStatus.BAD_REQUEST,
            )
        elif not user.email_is_confirmed:
            return make_error_response(
                msg=responses.EMAIL_IS_NOT_CONFIRMED,
                status=HTTPStatus.BAD_REQUEST,
            )
        refresh_token = jwt_service.create_refresh_token(user=user)

        token = jwt_service.create_access_token(user=user)

        save_activity(user, action=ActionsEnum.login)

        return Response(
            response=schemas.JWT(access_token=token, refresh_token=refresh_token).json(),
            status=HTTPStatus.OK,
            content_type='application/json',
        )


@jwt_tokens.route('/logout')
@jwt_tokens.expect(jwt_parser)
class JWTLogout(Resource):

    @log_activity(action=ActionsEnum.logout)
    @jwt_required()
    @jwt_tokens.response(code=int(HTTPStatus.NO_CONTENT), description=' ')
    @jwt_tokens.expect(logout_parser)
    def post(self):
        args = logout_parser.parse_args()

        jwt_service = get_jwt_service()
        refresh_token_service = get_refresh_token_service()

        token_jti = get_jwt()['jti']
        refresh_token_jti = get_jti(args['refresh_token'])

        jwt_service.block_token(cache_key=token_jti,
                                expire=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])

        token_id = refresh_token_service.filter(token=args['refresh_token'], _first=True).id
        refresh_token_service.delete(item_id=token_id)
        jwt_service.block_token(cache_key=refresh_token_jti,
                                expire=current_app.config['JWT_REFRESH_TOKEN_EXPIRES'])

        return Response(status=HTTPStatus.NO_CONTENT)


@jwt_tokens.route('/refresh')
@jwt_tokens.expect(jwt_parser)
class JWTRefresh(Resource):
    @log_activity()
    @jwt_tokens.expect(logout_parser)
    @jwt_required(refresh=True)
    @jwt_tokens.response(code=int(HTTPStatus.OK), description=' ', model=_JWTRefresh)
    def post(self):
        jwt_service = get_jwt_service()

        token = jwt_service.create_access_token(user=current_user)

        return Response(
            response=schemas.JWTRefresh(access_token=token).json(),
            status=HTTPStatus.OK,
            content_type='application/json',
        )


@jwt_tokens.route('/logout_everywhere')
@jwt_tokens.expect(jwt_parser)
class JWTLogoutEverywhere(Resource):

    @log_activity(action=ActionsEnum.logout_everywhere)
    @jwt_required()
    @jwt_tokens.response(code=int(HTTPStatus.NO_CONTENT), description=' ')
    @jwt_tokens.response(code=int(HTTPStatus.BAD_REQUEST), description=' ')
    @jwt_tokens.expect(logout_everywhere)
    def post(self):
        args = logout_parser.parse_args()

        jwt_service = get_jwt_service()
        user_service = get_user_service()
        refresh_token_service = get_refresh_token_service()

        user_id = get_jwt()['sub']
        user_db = user_service.get(item_id=user_id)
        # Передаваемый пароль не совпал с паролем в базе данных
        if not user_db.check_password(args.pop('password')):
            return Response(status=HTTPStatus.BAD_REQUEST)

        token_jti = get_jwt()['jti']

        jwt_service.block_token(
            cache_key=token_jti,
            expire=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
        )

        for token in refresh_token_service.get_refresh_tokens(user_id=user_id):
            jti = get_jti(token)
            refresh_token_service.delete(item_id=token.id)
            jwt_service.block_token(
                cache_key=jti,
                expire=current_app.config['JWT_REFRESH_TOKEN_EXPIRES'],
            )

        return Response(status=HTTPStatus.NO_CONTENT)
