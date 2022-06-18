from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from services.persons import PersonsService, get_persons_service
from schemas.v1_schemas import Person, Film

router = APIRouter()


@router.get("/search", response_model=list[Person])
async def search_persons(
        query: str,
        persons_service: PersonsService = Depends(get_persons_service),
) -> list[Person]:
    persons = await persons_service.search_persons(search=query)
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="persons not found"
        )
    return [Person(**person.dict()) for person in persons]


@router.get("/{person_id}/film")
async def films_by_person(
        person_id: str,
        person_service: PersonsService = Depends(get_persons_service),
) -> list[Film]:
    persons = await person_service.get_persons_by_id(person_id=person_id)
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="person not found",
        )
    # todo подключить сервис фильмов


@router.get("/{person_id}", response_model=list[Person])
async def get_person(
        person_id: str,
        person_service: PersonsService = Depends(get_persons_service),
) -> list[Person]:
    persons = await person_service.get_persons_by_id(person_id=person_id)
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="person not found",
        )
    return [Person(**person.dict()) for person in persons]
