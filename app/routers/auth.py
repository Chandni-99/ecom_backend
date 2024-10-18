from fastapi import APIRouter, Depends,status,Header
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from app.crud.auth import signup, login, get_refresh_token
from app.db.base_class import get_db
from app.schemas.auth import Signup, UserOut, OAuth2EmailRequestForm, TokenResponse

router = APIRouter(tags=["Auth"], prefix="/auth")
# limiter = Limiter(key_func=get_remote_address)

@router.post("/signup", status_code=status.HTTP_200_OK, response_model=UserOut)
# @limiter.limit("5/minute") # Allow 5 requests per minute
async def user_signup(
        user: Signup,
        db: Session = Depends(get_db)):
    return await signup(db, user)


@router.post("/token", status_code=status.HTTP_200_OK,response_model=TokenResponse)
# @limiter.limit("5/minute") # Allow 5 requests per minute
async def user_login(
        user_credentials: OAuth2EmailRequestForm = Depends(),
        db: Session = Depends(get_db)):
    return await login(user_credentials, db)


@router.post("/refresh", status_code=status.HTTP_200_OK)
# @limiter.limit("5/minute") # Allow 5 requests per minute
async def refresh_access_token(
        refresh_token: str = Header(),
        db: Session = Depends(get_db)):
    return await get_refresh_token(token=refresh_token, db=db)