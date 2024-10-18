from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.models import Review  # Assuming you have a Review model defined
from app.schemas.reviews import ReviewCreate, ReviewUpdate
from app.utils.responses import ResponseHandler


def create_review(db: Session, review: ReviewCreate):
    try:
        db_review = Review(**review.dict())
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return ResponseHandler.create_success(db_review.description, db_review.id, db_review)
    except IntegrityError as e:
        db.rollback()
        # return ResponseHandler.error(f"Failed to create review: {str(e)}")


def get_review(db: Session, review_id: int):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        return ResponseHandler.single_not_found_error("Review", review_id)
    return ResponseHandler.get_single_success("Review", review.id, review)


def get_reviews(db: Session, product_id: int):
    reviews = db.query(Review).filter(Review.product_id == product_id).all()
    if not reviews:
        return ResponseHandler.not_found_error("Reviews for this product")
    return ResponseHandler.success(f"Reviews for product with id {product_id}", reviews)


def update_review(db: Session, review_id: int, review_data: ReviewUpdate, user_id: int):
    review = db.query(Review).filter(Review.id == review_id, Review.user_id == user_id).first()
    if not review:
        return ResponseHandler.single_not_found_error("Review", review_id)

    for key, value in review_data.dict().items():
        setattr(review, key, value)
    db.commit()
    db.refresh(review)
    return ResponseHandler.update_success("Review", review.id, review)


def delete_review(db: Session, review_id: int, user_id: int):
    review = db.query(Review).filter(Review.id == review_id, Review.user_id == user_id).first()
    if not review:
        return ResponseHandler.single_not_found_error("Review", review_id)

    db.delete(review)
    db.commit()
    return ResponseHandler.delete_success("Review", review.id)
