from http import HTTPStatus

from fastapi import APIRouter, Depends
from pydantic import UUID4

from extensions.auth import security
from models.auth import AuthUser
from services.comments import CommentsService, get_comments_service

router = APIRouter()


@router.post(
    path='/{film_id}',
    description='Post comment',
    status_code=HTTPStatus.CREATED
)
async def add_comment_to_film(
        film_id: UUID4,
        comment: str,
        comments_service: CommentsService = Depends(get_comments_service),
        auth_user: AuthUser = Depends(security),
):
    await comments_service.add_comment(
        user_id=auth_user.uuid,
        film_id=film_id,
        comment=comment,
    )
