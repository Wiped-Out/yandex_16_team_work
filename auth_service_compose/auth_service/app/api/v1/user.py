from flask_restful import Resource, reqparse
from services.user import get_user_service
from flask import Response, request, jsonify
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from utils.utils import log_activity
from schemas import schemas
from sqlalchemy.exc import IntegrityError


class User(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("email", type=str)
        self.parser.add_argument("login", type=str)
        self.parser.add_argument("password", type=str)

        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument("password", type=str)
        self.put_parser.add_argument("login", type=str, required=False)
        self.put_parser.add_argument("email", type=str, required=False)
        self.put_parser.add_argument("new_password", type=str, required=False)
        self.put_parser.add_argument("new_password_repeat", required=False)

    @log_activity()
    @jwt_required()
    def post(self):
        user_service = get_user_service()
        db_user = user_service.create_user(params=self.parser.parse_args())

        return Response(
            response=schemas.User(**db_user.dict()).json(),
            status=HTTPStatus.CREATED,
            content_type="application/json",
        )

    @log_activity()
    @jwt_required()
    def get(self, user_id: str):
        user_service = get_user_service()

        user = user_service.get_user(
            user_id=user_id,
            cache_key=request.base_url
        )
        return jsonify(schemas.User(**user.dict()).dict())

    @log_activity()
    @jwt_required()
    def put(self, user_id: str):
        user_service = get_user_service()

        args = self.put_parser.parse_args()

        user_db = user_service.get(item_id=user_id)
        # Передаваемый пароль не совпал с паролем в базе данных
        if not user_db.check_password(args.pop("password")):
            return Response(status=HTTPStatus.BAD_REQUEST)

        new_password = args.pop("new_password")
        new_password_repeat = args.pop("new_password_repeat")
        if new_password or new_password_repeat:
            if new_password == new_password_repeat:
                user_service.update_password(user_id=user_id, password=new_password)
                return Response(status=HTTPStatus.NO_CONTENT)
            else:
                return Response(status=HTTPStatus.BAD_REQUEST)

        try:
            user_service.update(item_id=user_id, **args)
        except IntegrityError:
            return Response(status=HTTPStatus.CONFLICT)

        return Response(status=HTTPStatus.NO_CONTENT)
