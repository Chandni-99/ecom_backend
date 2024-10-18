from datetime import timedelta, datetime

from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.core.config import settings
from app.crud.user import get_user_by_id
from app.db.base_class import get_db
from app.models.models import User
from app.schemas.auth import TokenResponse, TokenData
from app.utils.responses import ResponseHandler

pwd_context =CryptContext(schemes=['bcrypt'],deprecated="auto")
# auth_scheme =HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)


# Create Access & Refresh Token
async def get_user_token(uuid: str, refresh_token=None):
    payload = {"id": uuid}

    ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    access_token = await create_access_token(payload, ACCESS_TOKEN_EXPIRE_MINUTES)

    if not refresh_token:
        refresh_token = await create_refresh_token(payload)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES
    )


# Create Access Token
async def create_access_token(data: dict,ACCESS_TOKEN_EXPIRE_MINUTES: int):
    payload = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# Create Refresh Token
async def create_refresh_token(data):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# Get Payload Of Token
def get_token_payload(token):
    try:
        return jwt.decode(token, settings.SECRET_KEY, [settings.ALGORITHM])
    except JWTError:
        raise ResponseHandler.invalid_token('access')


# def get_current_user(token):
#     user = get_token_payload(token.credentials)
#     return user.get('id')


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Extracts user from the Bearer token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        id = payload.get("id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception

    # Fetch the user from the database
    user = get_user_by_uuid(db, uuid=token_data.id)
    if user is None:
        raise credentials_exception
    return user

def get_user_by_uuid(db:Session,uuid:str):
    user =db.query(User).filter(User.uuid == uuid).first()
    if user:
        return user