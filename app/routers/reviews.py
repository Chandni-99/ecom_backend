from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.reviews import create_review, get_review, get_reviews, update_review, delete_review
from app.schemas.reviews import ReviewCreate, ReviewUpdate, ReviewOut, ReviewsOut, ReviewOutDelete
from app.db.base_class import get_db  # Assuming you have a method to get the DB session
from app.models.models import User  # Assuming you have a User model and an auth dependency


router = APIRouter(tags=["Reviews"], prefix="/reviews",dependencies=[Depends(get_current_user)])

# Create a review
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReviewOut)
async def create_review_route(
    review: ReviewCreate,
    db: Session = Depends(get_db) # Assuming you have a current user dependency
):
    return create_review(db, review)


# Get a single review
@router.get("/{review_id}", status_code=status.HTTP_200_OK, response_model=ReviewOut)
async def get_review_route(
    review_id: int,
    db: Session = Depends(get_db),
):
    return get_review(db, review_id)


# Get all reviews for a product
@router.get("/product/{product_id}", status_code=status.HTTP_200_OK, response_model=ReviewsOut)
async def get_reviews_route(
    product_id: int,
    db: Session = Depends(get_db),
):
    return get_reviews(db, product_id)


# Update a review
@router.put("/{review_id}", status_code=status.HTTP_200_OK, response_model=ReviewOut)
async def update_review_route(
    review_id: int,
    review_data: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_review(db, review_id, review_data, user_id=current_user.id)


# Delete a review
@router.delete("/{review_id}", status_code=status.HTTP_200_OK, response_model=ReviewOutDelete)
async def delete_review_route(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_review(db, review_id, user_id=current_user.id)
