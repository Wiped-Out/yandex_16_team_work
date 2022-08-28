from http import HTTPStatus

from api.answers.v1 import answers
from extensions.auth import security
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_pagination import Page
from models.auth import AuthUser
from schemas.pagination import PaginatedParams
from schemas.v1_schemas import FilmMainPage, Person
from services.films import FilmsService, get_films_service
from services.persons import PersonsService, get_persons_service
from utils import utils

router = APIRouter()


@router.get(
    path='/search',
    response_model=Page[Person],
    description='Search persons by query parameter',
)
async def search_persons(
        query: str, request: Request,
        persons_service: PersonsService = Depends(get_persons_service),
        paginated_params: PaginatedParams = Depends(),
        auth_user: AuthUser = Depends(security),
):
    page_size, page = paginated_params.page_size, paginated_params.page

    persons = await persons_service.search_persons(
        search=query, page_size=page_size, page=page, base_url=request.url.path,
    )
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=answers.PERSONS_NOT_FOUND,
        )

    total_records = await persons_service.count_persons(search=query)
    return utils.paginate(
        items=[Person(**person.dict()) for person in persons],
        total=total_records, page=page, size=page_size,
    )


@router.get(
    path='/{person_id}/film',
    response_model=Page[FilmMainPage],
    description='Get films where person was involved',
)
async def films_by_person(
        person_id: str,
        films_service: FilmsService = Depends(get_films_service),
        paginated_params: PaginatedParams = Depends(),
        auth_user: AuthUser = Depends(security),
):
    page_size, page = paginated_params.page_size, paginated_params.page
    films = await films_service.get_films_for_person(
        person_id=person_id, page=page, page_size=page_size,
    )
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=answers.FILMS_NOT_FOUND,
        )

    total_records = await films_service.count_films_for_person(person_id)
    return utils.paginate(
        items=[FilmMainPage(**film.dict()) for film in films],
        total=total_records, page=page, size=page_size,
    )


@router.get(
    path='/{person_id}',
    response_model=list[Person],
    description="Get person's full name, role and films where person was involved",
)
async def get_person(
        person_id: str, request: Request,
        person_service: PersonsService = Depends(get_persons_service),
        auth_user: AuthUser = Depends(security),
) -> list[Person]:
    persons = await person_service.get_persons_by_id(
        person_id=person_id, base_url=request.url.path,
    )
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=answers.PERSON_NOT_FOUND,
        )
    return [Person(**person.dict()) for person in persons]
