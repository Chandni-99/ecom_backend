from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.products import get_products, get_product_by_id, update_product_by_id, delete_product_by_id, \
    create_product
from app.db.base_class import get_db
from app.schemas.products import ProductCreate, ProductOut, ProductOutData, ProductsOut, ProductUpdate, ProductBase

router = APIRouter(tags=["Products"], prefix="/products",dependencies=[Depends(get_current_user)])

@router.post("/",response_model=ProductOut)
def create_products(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db,product)

@router.get("/",response_model=List[ProductBase])
def get_all_products( skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_products(db, skip=skip, limit=limit)

@router.get("/{product_id}",response_model=ProductOut)
def get_product(product_id :int , db: Session = Depends(get_db)):
    return get_product_by_id(db,product_id)

@router.put("/{product_id}",response_model=ProductOut)
def update_product(product_id: int,product: ProductUpdate, db:Session =Depends(get_db)):
    return update_product_by_id(db,product_id,product)

@router.delete("/{product_id}",response_model=ProductOut)
def delete_product(product_id: int, db:Session =Depends(get_db)):
    return delete_product_by_id(db,product_id)





