from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

from services.films import (
    FilmService, get_film_service, get_films_service, FilmsService
)
from typing import Optional
from schemas.v1_schemas import FilmMainPage
from models.film import Film

router = APIRouter()


@router.get("/search", response_model=FilmMainPage)
async def search_for_films(
        query: str, films_service: FilmsService = Depends(get_films_service),
        page_size: Optional[int] = Query(default=None, alias="page[size]"),
        page: Optional[int] = Query(default=None, alias="page[number]"),
):
    if not page_size:
        page_size = 50
    if not page:
        page = 1

    films = await films_service.get_films(
        search=query, page_size=page_size, page=page,
    )
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="films not found",
        )

    return [FilmMainPage(**film.dict()) for film in films]


@router.get('/{film_id}', response_model=Film)
async def film_details(
        film_id: str, film_service: FilmService = Depends(get_film_service)
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='film not found',
        )

    return Film(**film.dict())


@router.get('', response_model=list[Film])
async def get_films_for_main_page(
        films_service: FilmsService = Depends(get_films_service),
        sort: Optional[str] = None,
        genre_id: Optional[str] = Query(default=None, alias="filter[genre]"),
        page_size: Optional[int] = Query(default=None, alias="page[size]"),
        page: Optional[int] = Query(default=None, alias="page[number]"),
):
    if not page_size:
        page_size = 50
    if not page:
        page = 1

    films = await films_service.get_films(
        sort_param=sort, genre_id=genre_id, page=page,
        page_size=page_size,
    )
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="films not found",
        )

    return [Film(**film.dict()) for film in films]
