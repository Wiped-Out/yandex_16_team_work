from http import HTTPStatus

from extensions.auth import security
from fastapi import APIRouter, Depends
from models.auth import AuthUser
from pydantic import UUID4
from services.likes import LikesService, get_likes_service

router = APIRouter()


@router.post(
    path='/{film_id}',
    description='Give a like to the film',
    status_code=HTTPStatus.CREATED
)
async def give_like(
        film_id: UUID4,
        likes_service: LikesService = Depends(get_likes_service),
        auth_user: AuthUser = Depends(security),
):
    await likes_service.give_like(user_id=auth_user.uuid, film_id=film_id)
