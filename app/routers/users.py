from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.user import create_user, get_user_by_id, update_users, delete_user
from app.db.base_class import get_db
from app.schemas.users import UsersOut, UserCreate, UserUpdate, UserOut

router = APIRouter(tags=["Users"], prefix="/users",dependencies=[Depends(get_current_user)])

@router.post("/",response_model=UserOut)
def create_users(user:UserCreate,db:Session= Depends(get_db)):
    return create_user(db,user)

@router.get("/{user_id}",response_model=UserOut)
def get_user(user_id:int, db:Session =Depends(get_db)):
    return get_user_by_id(db,user_id)

@router.put("/{user_id}",response_model=UserOut)
def update_user(user_id: int,user: UserUpdate, db:Session =Depends(get_db)):
    return update_users(db,user_id,user)

@router.delete("/{user_id}",response_model=UserOut)
def delete_user(user_id: int, db:Session =Depends(get_db)):
    return delete_user(db,user_id)

