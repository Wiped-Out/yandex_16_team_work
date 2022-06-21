from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from services.films import (
    FilmService, get_film_service, get_films_service, FilmsService
)
from typing import Optional
from schemas.v1_schemas import Film
from models.film import Film
from fastapi_pagination import Page
from utils import utils

router = APIRouter()


@router.get("/search", response_model=Page[Film])
async def search_for_films(
        query: str, request: Request,
        films_service: FilmsService = Depends(get_films_service),
        page_size: Optional[int] = Query(default=50, alias="page[size]"),
        page: Optional[int] = Query(default=1, alias="page[number]"),
):
    cache_key = f"{request.url.path}_{query=}_{page_size=}_{page=}"
    films = await films_service.get_films(
        search=query, page_size=page_size, page=page, cache_key=cache_key,
    )
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="films not found",
        )

    total_records = await films_service.count_items_in_elastic(search=query)
    return utils.paginate(
        items=[Film(**film.dict()) for film in films],
        total=total_records, page=page, size=page_size
    )


@router.get('/{film_id}', response_model=Film)
async def film_details(
        film_id: str, request: Request,
        film_service: FilmService = Depends(get_film_service)
) -> Film:
    cache_key = f"{request.url.path}_{film_id=}"
    film = await film_service.get_by_id(film_id=film_id, cache_key=cache_key)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='film not found',
        )

    return Film(**film.dict())


@router.get('', response_model=Page[Film])
async def get_films_for_main_page(
        request: Request,
        films_service: FilmsService = Depends(get_films_service),
        sort: Optional[str] = None,
        genre_id: Optional[str] = Query(default=None, alias="filter[genre]"),
        page_size: Optional[int] = Query(default=50, alias="page[size]"),
        page: Optional[int] = Query(default=1, alias="page[number]"),
):
    cache_key = f"{request.url.path}_{sort=}_{page_size=}_{page=}"
    films = await films_service.get_films(
        sort_param=sort, genre_id=genre_id, page=page,
        page_size=page_size, cache_key=cache_key,
    )
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="films not found",
        )

    total_records = await films_service.count_items_in_elastic(genre_id=genre_id)
    return utils.paginate(
        items=[Film(**film.dict()) for film in films],
        total=total_records, page=page, size=page_size,
    )
