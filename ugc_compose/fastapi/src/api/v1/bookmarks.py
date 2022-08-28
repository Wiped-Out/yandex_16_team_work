from http import HTTPStatus

from extensions.auth import security
from fastapi import APIRouter, Depends, Response
from models.auth import AuthUser
from pydantic import UUID4
from services.bookmarks import BookmarksService, get_bookmarks_service

router = APIRouter()


@router.post(
    path='/{film_id}',
    description='Save film to watch later (add bookmark)',
)
async def add_bookmark(
        film_id: UUID4,
        bookmarks_service: BookmarksService = Depends(get_bookmarks_service),
        auth_user: AuthUser = Depends(security),
):
    await bookmarks_service.add_bookmark(user_id=auth_user.uuid, film_id=film_id)

    return Response(status_code=HTTPStatus.CREATED)
