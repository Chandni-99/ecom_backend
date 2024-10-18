from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.users import TimestampBase


# Base schema for Cart
class CartBase(BaseModel):
    id: int
    total_amount: float
    user_id: int  # Foreign key to the user
    quantity : int

    class Config:
        from_attributes = True

# Output data for Cart without timestamps
class CartOutData(BaseModel):
    id: int
    total_amount: float
    quantity: int
    
    class Config:
        from_attributes = True

class CartCreate(CartBase):
    quantity : int

    class Config:
        from_attributes = True

class CartUpdate(CartCreate):
    pass  # You can add specific fields for updating if necessary

# Cart response classes
class CartOut(BaseModel):
    message: str
    data: CartOutData  # Use the CartOutData schema

    class Config:
        from_attributes = True

class CartsOut(BaseModel):
    message: str
    data: List[CartOutData]  # List of CartOutData

    class Config:
        from_attributes = True

class CartOutDelete(BaseModel):
    message: str
    id: int  # Only include the id of the deleted cart

    class Config:
        from_attributes = True
