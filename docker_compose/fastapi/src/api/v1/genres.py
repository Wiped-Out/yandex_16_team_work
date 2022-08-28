from http import HTTPStatus

from api.answers.v1 import answers
from extensions.auth import security
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_pagination import Page
from models.auth import AuthUser
from schemas.pagination import PaginatedParams
from schemas.v1_schemas import Genre
from services.genres import (GenreService, GenresService, get_genre_service,
                             get_genres_service)
from utils import utils

router = APIRouter()


@router.get(
    path='/{genre_id}',
    response_model=Genre,
    description='Get genre name by UUID',
)
async def get_genre(
        genre_id: str, request: Request,
        genre_service: GenreService = Depends(get_genre_service),
        auth_user: AuthUser = Depends(security),
) -> Genre:

    genre = await genre_service.get_genre(
        genre_id=genre_id, base_url=request.url.path,
    )
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=answers.GENRE_NOT_FOUND,
        )

    return Genre(**genre.dict())


@router.get(
    path='',
    response_model=Page[Genre],
    description='Get all genres',
)
async def get_genres(
        request: Request,
        genres_service: GenresService = Depends(get_genres_service),
        paginated_params: PaginatedParams = Depends(),
        auth_user: AuthUser = Depends(security),
):
    page_size, page = paginated_params.page_size, paginated_params.page

    genres_from_db = await genres_service.get_genres(
        page_size=page_size, page=page, base_url=request.url.path,
    )
    if not genres_from_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=answers.GENRES_NOT_FOUND,
        )

    total_records = await genres_service.count_all_data_in_index(index='genres')
    return utils.paginate(
        items=[Genre(**genre.dict()) for genre in genres_from_db],
        total=total_records, page=page, size=page_size,
    )
