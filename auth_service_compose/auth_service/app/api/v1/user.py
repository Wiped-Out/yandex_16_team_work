import json
from http import HTTPStatus

from flask import Response, request, jsonify
from flask_jwt_extended import jwt_required
from flask_restx import Resource, reqparse, fields, Namespace
from sqlalchemy.exc import IntegrityError

from api.v1.__base__ import base_url
from extensions.jwt import jwt_parser
from schemas.v1 import schemas
from services.user import get_user_service
from services.user_roles import get_user_roles_service
from utils.utils import log_activity, make_error_response
from api.responses import responses

user = Namespace('User', path=f"{base_url}/users", description='')

_User = user.model("user",
                   {
                       "id": fields.String,
                       "login": fields.String,
                       "email": fields.String
                   }
                   )

NestedUser = user.model("NestedUser",
                        {
                            "items": fields.Nested(_User, as_list=True)
                        })

user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument("email", type=str, location='json')
user_post_parser.add_argument("login", type=str, location='json')
user_post_parser.add_argument("password", type=str, location='json')

user_put_parser = reqparse.RequestParser()
user_put_parser.add_argument("password", type=str, location='json')
user_put_parser.add_argument("login", type=str, required=False, location='json')
user_put_parser.add_argument("email", type=str, required=False, location='json')
user_put_parser.add_argument("new_password", type=str, required=False, location='json')
user_put_parser.add_argument("new_password_repeat", required=False, location='json')

user_roles_parser = reqparse.RequestParser()
user_roles_parser.add_argument("role_id", type=str, location='json')


@user.route("/")
@user.expect(jwt_parser)
class Users(Resource):
    @jwt_required()
    @log_activity()
    @user.response(code=int(HTTPStatus.OK), description=" ", model=NestedUser)
    def get(self) -> Response:
        user_service = get_user_service()
        cache_key = request.base_url

        db_users = user_service.get_users(cache_key=cache_key)
        return jsonify(
            {"items": [schemas.User(**db_user.dict()).dict() for db_user in db_users]}
        )

    @log_activity()
    @jwt_required()
    @user.response(code=int(HTTPStatus.CREATED), description=" ", model=_User)
    @user.expect(user_post_parser)
    def post(self):
        user_service = get_user_service()
        try:
            db_user = user_service.create_user(params=user_post_parser.parse_args())
        except IntegrityError:
            return make_error_response(
                status=HTTPStatus.BAD_REQUEST,
                msg=responses.USER_ALREADY_EXIST,
            )

        return Response(
            response=schemas.User(**db_user.dict()).json(),
            status=HTTPStatus.CREATED,
            content_type="application/json",
        )


@user.route("/<user_id>")
@user.expect(jwt_parser)
class UserId(Resource):
    @log_activity()
    @jwt_required()
    @user.response(code=int(HTTPStatus.OK), description=" ", model=_User)
    def get(self, user_id: str):
        user_service = get_user_service()

        user = user_service.get_user(
            user_id=user_id,
            cache_key=request.base_url
        )
        return jsonify(schemas.User(**user.dict()).dict())

    @log_activity()
    @jwt_required()
    @user.response(code=int(HTTPStatus.NO_CONTENT), description=" ")
    @user.response(code=int(HTTPStatus.BAD_REQUEST), description=" ")
    @user.response(code=int(HTTPStatus.CONFLICT), description=" ")
    @user.expect(user_put_parser)
    def put(self, user_id: str):
        user_service = get_user_service()

        args = user_put_parser.parse_args()

        user_db = user_service.get(item_id=user_id)
        # Передаваемый пароль не совпал с паролем в базе данных
        if not user_db.check_password(args.pop("password")):
            return make_error_response(
                status=HTTPStatus.BAD_REQUEST,
                msg=responses.INCORRECT_PASSWORD,
            )

        new_password = args.pop("new_password")
        new_password_repeat = args.pop("new_password_repeat")
        if new_password or new_password_repeat:
            if new_password != new_password_repeat:
                return make_error_response(
                    status=HTTPStatus.BAD_REQUEST,
                    msg=responses.PASSWORDS_DID_NOT_MATCH,
                )

            user_service.update_password(user_id=user_id, password=new_password)

        try:
            args = {key: value for key, value in args.items() if value}

            if args:
                user_service.update(item_id=user_id, **args)
        except IntegrityError:
            return make_error_response(
                status=HTTPStatus.CONFLICT,
                msg=responses.CANT_UPDATE_USER,
            )

        return Response(
            response=json.dumps({}),
            status=HTTPStatus.NO_CONTENT,
            content_type="application/json",
        )


@user.route("/<user_id>/role")
class UserRoleCreate(Resource):
    @log_activity()
    @jwt_required()
    @user.response(code=int(HTTPStatus.NO_CONTENT), description=" ")
    @user.response(code=int(HTTPStatus.BAD_REQUEST), description=" ")
    @user.response(code=int(HTTPStatus.CONFLICT), description=" ")
    def post(self, user_id: str):
        user_roles_service = get_user_roles_service()

        try:
            user_roles_service.add_role_to_user(
                user_id,
                **user_roles_parser.parse_args()
            )
        except IntegrityError:
            return make_error_response(
                status=HTTPStatus.CONFLICT,
                msg=responses.CANT_ADD_ROLE_TO_USER,
            )

        return Response(
            response=json.dumps({}),
            status=HTTPStatus.NO_CONTENT,
            content_type="application/json",
        )


@user.route("/<user_id>/role/<role_id>")
class UserRoleDelete(Resource):
    @log_activity()
    @jwt_required()
    @user.response(code=int(HTTPStatus.NO_CONTENT), description=" ")
    def delete(self, user_id: str, role_id: str):
        user_roles_service = get_user_roles_service()

        try:
            user_roles_service.delete_role_from_user(
                user_id=user_id, role_id=role_id,
            )
        except IntegrityError:
            return make_error_response(
                status=HTTPStatus.CONFLICT,
                msg=responses.CANT_DELETE_ROLE_FROM_USER,
            )

        return Response(
            response=json.dumps({}),
            status=HTTPStatus.NO_CONTENT,
            content_type="application/json",
        )
