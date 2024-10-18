from pydantic import  EmailStr
from app.schemas.users import BaseConfig
from pydantic import BaseModel


class OAuth2EmailRequestForm(BaseModel):
    email: str
    password: str

class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    is_active: bool
    # carts: List[CartBase]

    class Config(BaseConfig):
        pass


class Signup(BaseModel):
    username: str
    email: str
    password: str

    class Config(BaseConfig):
        pass


class UserOut(BaseModel):
    message: str
    data: UserBase

    class Config(BaseConfig):
        pass


# Token
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'

class TokenData(BaseModel):
    id:str