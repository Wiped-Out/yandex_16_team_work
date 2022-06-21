from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from services.persons import PersonsService, get_persons_service
from services.films import FilmsService, get_films_service
from schemas.v1_schemas import Person, Film
from typing import Optional
from utils import utils
from fastapi_pagination import Page

router = APIRouter()


@router.get("/search", response_model=Page[Person])
async def search_persons(
        query: str,
        persons_service: PersonsService = Depends(get_persons_service),
        page_size: Optional[int] = Query(default=50, alias="page[size]"),
        page: Optional[int] = Query(default=1, alias="page[number]"),
):
    persons = await persons_service.search_persons(
        search=query, page_size=page_size, page=page,
    )
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="persons not found"
        )

    total_records = await persons_service.count_persons_in_elastic(search=query)
    return utils.paginate(
        items=[Person(**person.dict()) for person in persons],
        total=total_records, page=page, size=page_size
    )


@router.get("/{person_id}/film", response_model=Page[Film])
async def films_by_person(
        person_id: str,
        films_service: FilmsService = Depends(get_films_service),
        page_size: Optional[int] = Query(default=50, alias="page[size]"),
        page: Optional[int] = Query(default=1, alias="page[number]"),
):
    films = await films_service.get_films_for_person(
        person_id=person_id, page=page, page_size=page_size,
    )
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="films not found",
        )

    total_records = await films_service.count_films_for_person_in_elastic(person_id)
    return utils.paginate(
        items=[Film(**film.dict()) for film in films],
        total=total_records, page=page, size=page_size
    )


@router.get("/{person_id}", response_model=list[Person])
async def get_person(
        person_id: str,
        person_service: PersonsService = Depends(get_persons_service),
) -> list[Person]:
    persons = await person_service._get_persons_by_id(person_id=person_id)
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="person not found",
        )
    return [Person(**person.dict()) for person in persons]
