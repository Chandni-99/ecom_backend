from typing import List

from sqlalchemy.orm import Session
from app.models.models import Product
from app.schemas.products import ProductCreate, ProductsOut, ProductUpdate, ProductBase
from app.utils.responses import ResponseHandler

def create_product(db:Session, product:ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return ResponseHandler.create_success(db_product.title, db_product.id, db_product)

def get_products(db:Session, skip: int = 0, limit: int = 10)-> List[ProductBase]:
    products = db.query(Product).offset(skip).limit(limit).all()
    if not products:
        return ResponseHandler.not_found_error("Products")  # Use your response handler
    return [ProductBase.from_orm(product) for product in products]

def get_product_by_id(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()  # Corrected filter syntax
    if not product:
        return ResponseHandler.single_not_found_error("Product", product_id)  # Use your response handler
    return ResponseHandler.get_single_success("Product", product_id, product)

def update_product_by_id(db:Session, product_id: int, product :ProductUpdate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        return ResponseHandler.single_not_found_error("Product", product_id)
    for key,val in product.dict().items():
        setattr(db_product,key,val)
    db.commit()
    db.refresh(db_product)
    return ResponseHandler.update_success("Product", product_id, db_product)

def delete_product_by_id(db:Session, product_id: int):
    db_product = db.query(Product).filter(product_id==product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return ResponseHandler.delete_success("Product", product_id, db_product)  # Use your response handler

    return ResponseHandler.single_not_found_error("Product", product_id)  # Return not found if product doesn't exist
