from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from services.genres import (
    GenresService, get_genres_service, GenreService, get_genre_service,
)
from schemas.v1_schemas import Genre

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


@router.get("", response_model=Genre)
async def get_genres(
        genres_service: GenresService = Depends(get_genres_service)
) -> list[Genre]:
    genres_from_db = await genres_service.get_genres()
    if not genres_from_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genres not found")

    return [Genre(**genre.dict()) for genre in genres_from_db]
