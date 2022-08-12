from http import HTTPStatus

from fastapi import APIRouter, Depends, Response
from services.film_progress import FilmProgressService, get_film_progress_service

from models.auth import AuthUser
from extensions.auth import security
from pydantic import UUID4

router = APIRouter()


@router.post(
    path="/{film_id}",
    description="Save film watch progress"
)
async def add_film_progress(
        film_id: UUID4,
        seconds: int,
        film_progress_service: FilmProgressService = Depends(get_film_progress_service),
        auth_user: AuthUser = Depends(security),
):
    await film_progress_service.save_film_progress(
        user_id=auth_user.uuid, film_id=film_id, seconds=seconds,
    )

    return Response(status_code=HTTPStatus.CREATED)
