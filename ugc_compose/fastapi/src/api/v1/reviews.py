import uuid
from http import HTTPStatus

from extensions.auth import security
from fastapi import APIRouter, Depends, Response
from models.auth import AuthUser
from pydantic import UUID4
from services.reviews import ReviewsService, get_reviews_service

router = APIRouter()


@router.post(
    path='/{film_id}',
    description='Post review',
)
async def add_review_to_film(
        film_id: UUID4,
        text: str,
        reviews_service: ReviewsService = Depends(get_reviews_service),
        auth_user: AuthUser = Depends(security),
):
    review_id = await reviews_service.add_review(
        user_id=auth_user.uuid,
        film_id=film_id,
        text=text
    )

    return Response(content=review_id, status_code=HTTPStatus.CREATED)


@router.post(
    path='/reaction/{review_id}',
    description='Post reaction on review'
)
async def add_reaction_to_review(
    review_id: str,
    reaction: str,
    reviews_service: ReviewsService = Depends(get_reviews_service),
    auth_user: AuthUser = Depends(security),
):
    await reviews_service.add_reaction(
        user_id=auth_user.uuid,
        review_id=review_id,
        reaction=reaction
    )

    return Response(status_code=HTTPStatus.CREATED)
