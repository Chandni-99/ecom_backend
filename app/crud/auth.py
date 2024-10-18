from fastapi import Depends, HTTPException,status
from fastapi.security import  OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, get_user_token, get_token_payload
from app.db.base_class import get_db
from app.models.models import User
from app.schemas.auth import Signup, OAuth2EmailRequestForm
from app.utils.responses import ResponseHandler

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def login(user_credentials: OAuth2EmailRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    return await get_user_token(uuid=user.uuid)

async def signup(db: Session, user: Signup):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    db_user = User(id=None, **user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return ResponseHandler.create_success(db_user.username, db_user.id, db_user)


async def get_refresh_token(token, db):
    payload = get_token_payload(token)
    user_id = payload.get('id', None)
    if not user_id:
        raise ResponseHandler.invalid_token('refresh')

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ResponseHandler.invalid_token('refresh')

    return await get_user_token(uuid=user.uuid, refresh_token=token)