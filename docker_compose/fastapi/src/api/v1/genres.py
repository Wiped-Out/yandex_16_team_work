from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from services.genres import (
    GenresService, get_genres_service, GenreService, get_genre_service,
)
from schemas.v1_schemas import Genre
from fastapi_pagination import Page
from utils import utils
from typing import Optional

router = APIRouter()


@router.get("/{genre_id}", response_model=Genre)
async def get_genre(
        genre_id: str,
        genre_service: GenreService = Depends(get_genre_service)
) -> Genre:
    genre = await genre_service.get_genre(genre_id=genre_id)
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="genre not found",
        )

    return Genre(**genre.dict())


@router.get("", response_model=Page[Genre])
async def get_genres(
        genres_service: GenresService = Depends(get_genres_service),
        page_size: Optional[int] = Query(default=50, alias="page[size]"),
        page: Optional[int] = Query(default=1, alias="page[number]"),
):
    genres_from_db = await genres_service.get_genres(
        page_size=page_size, page=page,
    )
    if not genres_from_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="genres not found",
        )

    total_records = await genres_service.count_genres_in_elastic()
    return utils.paginate(
        items=[Genre(**genre.dict()) for genre in genres_from_db],
        total=total_records, page=page, size=page_size,
    )
