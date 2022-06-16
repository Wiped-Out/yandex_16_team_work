from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from pydantic.types import UUID4

from services.films import (
    FilmService, get_film_service, get_films_service, FilmsService
)
from typing import Optional
from models import genre, person

router = APIRouter()


class FilmPage(BaseModel):
    title: str
    imdb_rating: Optional[float] = 0.01
    description: str
    genres: Optional[list[genre.Genre]]
    actors: Optional[list[person.Person]]
    screenwriters: Optional[list[person.Person]]
    director: Optional[person.Person]


class FilmMainPage(BaseModel):
    id: UUID4
    title: str
    imdb_rating: Optional[float] = 0.01


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


@router.get("/films/search")
async def search_for_films(
        query: str, films_service: FilmsService = Depends(get_films_service),
) -> list[FilmMainPage]:
    films = await films_service.get_films(search=query)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="films not found")

    return [FilmMainPage(**film.dict()) for film in films]
