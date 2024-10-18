from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.schemas.users import BaseConfig

# Base schema for category without timestamps (used for all responses)
class CategoryOutData(BaseModel):
    id: int
    name: str
    deleted_at :Optional[datetime]

    class Config(BaseConfig):
        pass

# Schema for creating categories (timestamps handled internally, not exposed)
class CategoryCreate(BaseModel):
    name: str

    class Config(BaseConfig):
        pass

# Schema for updating categories
class CategoryUpdate(CategoryCreate):
    pass

# Response for a single category (without timestamps)
class CategoryOut(BaseModel):
    msg: str
    data: CategoryOutData

    class Config(BaseConfig):
        pass

# Response for multiple categories (without timestamps)
class CategoriesOut(BaseModel):
    msg: str
    data: List[CategoryOutData]

    class Config(BaseConfig):
        pass

# Response for category deletion (without timestamps)
class CategoryOutDelete(BaseModel):
    message: str
    data: CategoryOutData

    class Config(BaseConfig):
        pass
