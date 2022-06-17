from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

from services.films import (
    FilmService, get_film_service, get_films_service, FilmsService
)
from typing import Optional
from schemas.v1_schemas import FilmPage, FilmMainPage

router = APIRouter()


@router.get("/films/search")
async def search_for_films(
        query: str, films_service: FilmsService = Depends(get_films_service),
) -> list[FilmMainPage]:
    films = await films_service.get_films(search=query)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="films not found")

    return [FilmMainPage(**film.dict()) for film in films]


@router.get('/films/{film_id}', response_model=FilmPage)
async def film_details(
        film_id: str, film_service: FilmService = Depends(get_film_service)
) -> FilmPage:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return FilmPage(
        title=film.title, description=film.description, genres=film.genres,
        actors=film.actors, screenwriters=film.screenwriters,
        director=film.director
    )


@router.get('/films')
async def get_films_for_main_page(
        films_service: FilmsService = Depends(get_films_service),
        sort: Optional[str] = None,
        genre_id: Optional[str] = Query(default=None, alias="filter[genre]")
):
    if sort:
        films = await films_service.get_films(sort_param=sort)
        if not films:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="films not found")

        return [FilmMainPage(**film.dict()) for film in films]

    # todo
    if genre_id:
        return genre_id
        pass
