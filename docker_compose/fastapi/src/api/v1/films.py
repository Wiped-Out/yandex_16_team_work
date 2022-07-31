from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi_pagination import Page

from api.answers.v1 import answers
from extensions.auth import security
from models.auth import AuthUser
from models.film import Film
from schemas.pagination import PaginatedParams
from schemas.v1_schemas import FilmMainPage
from services.films import (
    FilmService, get_film_service, get_films_service, FilmsService
)
from utils import utils

router = APIRouter()


@router.get(
    path="/search",
    response_model=Page[FilmMainPage],
    description="Search films by query parameter",
)
async def search_for_films(
        query: str, request: Request,
        films_service: FilmsService = Depends(get_films_service),
        paginated_params: PaginatedParams = Depends(),
        auth_user: AuthUser = Depends(security)
):
    page_size, page = paginated_params.page_size, paginated_params.page
    print(auth_user)
    cache_key = f"{request.url.path}_{query=}_{page_size=}_{page=}"
    films = await films_service.get_films(
        search=query, page_size=page_size, page=page, cache_key=cache_key,
    )
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=answers.FILMS_NOT_FOUND,
        )

    total_records = await films_service.count_items(search=query)
    return utils.paginate(
        items=[FilmMainPage(**film.dict()) for film in films],
        total=total_records, page=page, size=page_size
    )


@router.get(
    path='/{film_id}',
    response_model=Film,
    summary="Get info about film by UUID",
    description="Get title and IMDB rating for film"
)
async def film_details(
        film_id: str, request: Request,
        film_service: FilmService = Depends(get_film_service),
        auth_user: AuthUser = Depends(security)
):
    cache_key = f"{request.url.path}_{film_id=}"
    film = await film_service.get_film_by_id(film_id=film_id, cache_key=cache_key)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=answers.FILM_NOT_FOUND,
        )

    return Film(**film.dict())


@router.get(
    path='',
    response_model=Page[FilmMainPage],
    summary="Get films for main page",
    description="Get films info for main page: title and IMDB rating"
)
async def get_films_for_main_page(
        request: Request,
        films_service: FilmsService = Depends(get_films_service),
        sort: Optional[str] = None,
        genre_id: Optional[str] = Query(default=None, alias="filter[genre]"),
        paginated_params: PaginatedParams = Depends(),
        auth_user: AuthUser = Depends(security)
):
    page_size, page = paginated_params.page_size, paginated_params.page

    cache_key = f"{request.url.path}_{sort=}_{page_size=}_{page=}"
    films = await films_service.get_films(
        sort_param=sort, genre_id=genre_id, page=page,
        page_size=page_size, cache_key=cache_key
    )
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=answers.FILMS_NOT_FOUND,
        )

    total_records = await films_service.count_items(genre_id=genre_id)
    return utils.paginate(
        items=[FilmMainPage(**film.dict()) for film in films],
        total=total_records, page=page, size=page_size,
    )
