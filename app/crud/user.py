import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.users import UserCreate, UserOut, UserUpdate
from app.utils.responses import ResponseHandler

def create_user(db:Session,user:UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_uuid = str(uuid.uuid4())
    db_user = User(uuid=user_uuid,**user.dict())
    db.add(db_user)
    # try:
    db.commit()
    db.refresh(db_user)
    # except Exception as e:
    #     db.rollback()
    #     raise HTTPException(status_code=500, detail=str(e))
    return ResponseHandler.create_success("User", db_user.id, db_user)

def get_user_by_id(db:Session,user_id:int):
    user =db.query(User).filter(User.id == user_id).first()
    if not user:
        return ResponseHandler.single_not_found_error("User",user_id)
    return ResponseHandler.get_single_success(user.username, user_id, user)

# def get_users(db:Session,skip: int = 0, limit: int = 10):
#     users =db.query(User).offset(skip).limit(limit).all()
#     if not users:
#         return ResponseHandler.not_found_error("Users")
#     return users

def update_users(db:Session,user_id:int,user:UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return ResponseHandler.single_not_found_error("User", user_id)
    for key,val in user.dict().items():
        setattr(db_user,key,val)
    db.commit()
    db.refresh(db_user)
    return ResponseHandler.update_success("User",user_id,db_user)

def delete_user(db:Session,user_id:int):
    db_user =db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return ResponseHandler.delete_success("User", user_id, db_user)
    return ResponseHandler.single_not_found_error("User",user_id)





