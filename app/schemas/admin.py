from typing import Optional
from pydantic import BaseModel, EmailStr

from app.schemas.users import TimestampBase, BaseConfig

# Base schema for admin without timestamps for output
class AdminOutData(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config(BaseConfig):
        pass

# Base schema for admin (for creating/updating)
class AdminBase(TimestampBase):
    password: str

    class Config(BaseConfig):
        pass

# Schema for creating admins
class AdminCreate(AdminBase):
    username: str
    email: str

    class Config(BaseConfig):
        pass

# Schema for updating admins
class AdminUpdate(AdminCreate):
    password: Optional[str]  # Make password optional for updates

    class Config(BaseConfig):
        pass

# Response for admin deletion (without timestamps)
class AdminOutDelete(BaseModel):
    message: str
    id: int  # Only include the id of the deleted admin

    class Config(BaseConfig):
        pass
