from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from services.persons import (
    PersonsService, get_persons_service, PersonService, get_person_service
)
from schemas.v1_schemas import Person, Film

router = APIRouter()


@router.get("/search", response_model=list[Person])
async def search_persons(
        query: str,
        persons_service: PersonsService = Depends(get_persons_service),
) -> list[Person]:
    persons = await persons_service.get_persons(search_param=query)
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="persons not found"
        )
    return [Person(**person.dict()) for person in persons]


@router.get("/{person_id}/film")
async def films_by_person(
        person_id: str,
        person_service: PersonService = Depends(get_person_service),
) -> list[Film]:
    person = await person_service.get_person(person_id=person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="person not found",
        )
    # todo подключить сервис фильмов


@router.get("/{person_id}", response_model=Person)
async def get_person(
        person_id: str,
        person_service: PersonService = Depends(get_person_service),
) -> Person:
    person = await person_service.get_person(person_id=person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="person not found",
        )
    return Person(**person.dict())
