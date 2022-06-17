from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from services.persons import (
    PersonsService, get_persons_service, PersonService, get_person_service
)
from schemas.v1_schemas import Person, Film

router = APIRouter()


@router.get("/persons/search", response_model=Person)
async def search_persons(
        search_param: str,
        persons_service: PersonsService = Depends(get_persons_service),
) -> list[Person]:
    persons = await persons_service.get_persons(search_param=search_param)
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="persons not found"
        )
    return [Person(**person.dict()) for person in persons]


@router.get("/persons/{person_id}/film")
async def films_by_person(
        person_id: str,
) -> list[Film]:
    # todo
    pass


@router.get("/persons/{person_id}", response_model=Person)
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
