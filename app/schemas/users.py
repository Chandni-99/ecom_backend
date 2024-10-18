from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class TimestampBase(BaseModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = None

class BaseConfig:
    from_attributes = True  # Enables the use of ORM models for input/output

class UserOutData(BaseModel):
    # uuid:str
    id: int  # Use UUID here
    username: str
    email: EmailStr
    is_active: bool

    class Config(BaseConfig):
        pass

class UserCreate(BaseModel):
    username: str  # Make this required
    email: EmailStr
    password: str

    class Config(BaseConfig):
        pass

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserOut(BaseModel):
    message: str
    data: UserOutData

    class Config(BaseConfig):
        pass

class UsersOut(BaseModel):
    message: str
    data: List[UserOutData]

    class Config(BaseConfig):
        pass

class UserOutDelete(BaseModel):
    message: str
    data: UserOutData

    class Config(BaseConfig):
        pass
