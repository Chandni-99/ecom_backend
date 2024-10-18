from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.categories import (
    create_category,
    get_categories,
    get_category_by_id,
    update_category_by_id,
    delete_category_by_id,
)
from app.db.base_class import get_db
from app.schemas.categories import CategoryOut, CategoryCreate, CategoriesOut, CategoryUpdate

router = APIRouter(tags=["Categories"], prefix="/categories",dependencies=[Depends(get_current_user)])

@router.post("/", response_model=CategoryOut)
def create_categories(category: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, category)

@router.get("/", response_model=CategoriesOut)
def get_all_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_categories(db, skip=skip, limit=limit)

@router.get("/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    return get_category_by_id(db, category_id)

@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    return update_category_by_id(db, category_id, category)

@router.delete("/{category_id}", response_model=CategoryOut)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    return delete_category_by_id(db, category_id)
