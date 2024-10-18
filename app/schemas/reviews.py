from typing import  List
from pydantic import BaseModel, conint

from app.schemas.users import TimestampBase


# Base schema for Review
class ReviewBase(TimestampBase):
    id: int
    rating: conint(ge=1, le=5)  # Assuming rating is between 1 and 5
    description: str
    user_id: int  # Foreign key to the user
    product_id: int  # Foreign key to the product

    class Config:
        from_attributes = True

# Output data for Review without timestamps
class ReviewOutData(BaseModel):
    rating: int
    description: str
    user_id: int  # Include user ID for reference
    product_id: int  # Include product ID for reference

    class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    rating: conint(ge=1, le=5)  # Rating must be between 1 and 5
    description: str
    product_id: int  # Foreign key to the product

    class Config:
        from_attributes = True

class ReviewUpdate(ReviewCreate):
    pass  # You can add specific fields for updating if necessary

# Review response classes
class ReviewOut(BaseModel):
    message: str
    data: ReviewOutData  # Use the ReviewOutData schema

    class Config:
        from_attributes = True

class ReviewsOut(BaseModel):
    message: str
    data: List[ReviewOutData]  # List of ReviewOutData

    class Config:
        from_attributes = True

class ReviewOutDelete(BaseModel):
    message: str
    id: int  # Only include the id of the deleted review

    class Config:
        from_attributes = True
