from http import HTTPStatus

from fastapi import APIRouter, Depends
from pydantic import UUID4

from extensions.auth import security
from models.auth import AuthUser
from services.reviews import ReviewsService, get_reviews_service, ReactionType

router = APIRouter()


@router.post(
    path='/{film_id}',
    description='Post review',
    status_code=HTTPStatus.CREATED
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

    return {'id': review_id}


@router.post(
    path='/reaction/{review_id}',
    description='Post reaction on review',
    status_code=HTTPStatus.CREATED
)
async def add_reaction_to_review(
        review_id: str,
        reaction: ReactionType,
        reviews_service: ReviewsService = Depends(get_reviews_service),
        auth_user: AuthUser = Depends(security),
):
    await reviews_service.add_reaction(
        user_id=auth_user.uuid,
        review_id=review_id,
        reaction=reaction
    )
