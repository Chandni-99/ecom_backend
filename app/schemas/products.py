from typing import Optional, List
from pydantic import BaseModel, HttpUrl, conint

from app.schemas.users import BaseConfig, TimestampBase


# Base schema for product without timestamps
class ProductOutData(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: float
    discount_percentage: conint(ge=0, le=100) = 0
    brand: str
    image_url: Optional[HttpUrl] = None

    class Config(BaseConfig):
        pass

# Base schema for product (for creating/updating)
class ProductBase(BaseModel):
    title: str
    description: Optional[str]
    price: float
    discount_percentage: conint(ge=0, le=100) = 0
    brand: str
    image_url: Optional[HttpUrl] = None

    class Config(BaseConfig):
        pass

# Schema for creating products
class ProductCreate(ProductBase):
    category_id : int

# Schema for updating products
class ProductUpdate(ProductCreate):
    pass

# Response for a single product (without timestamps)
class ProductOut(BaseModel):
    message: str
    data: ProductOutData  # Use ProductOutData here

    class Config(BaseConfig):
        pass

# Response for multiple products (without timestamps)
class ProductsOut(BaseModel):
    message: str
    data: List[ProductOutData]
    # Use ProductOutData here

    class Config(BaseConfig):
        pass

# Response for product deletion (without timestamps)
class ProductOutDelete(BaseModel):
    message: str
    data: ProductOutData  # Use ProductOutData here

    class Config(BaseConfig):
        pass
