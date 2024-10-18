from sqlalchemy.orm import Session
from app.models.models import Category
from app.schemas.categories import CategoryCreate, CategoryOut, CategoryUpdate,CategoriesOut
from app.utils.responses import ResponseHandler

def create_category(db:Session, category:CategoryCreate):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return ResponseHandler.create_success(db_category.name, db_category.id, db_category)
    # return ResponseHandler.create_success(db_product.title, db_product.id, db_product)

def get_categories(db:Session, skip: int = 0, limit: int = 10):
    category = db.query(Category).offset(skip).limit(limit).all()
    if not category:
        return ResponseHandler.not_found_error("Categories")  # Use your response handler
    return category

def get_category_by_id(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()  # Corrected filter syntax
    if not category:
        return ResponseHandler.single_not_found_error("Category", category_id)  # Use your response handler
    return ResponseHandler.get_single_success("Product", category_id, category)

def update_category_by_id(db:Session, category_id: int, category :CategoryUpdate):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        return ResponseHandler.single_not_found_error("Category", category_id)
    for key,val in category().dict().items():
        setattr(db_category,key,val)
    db.commit()
    db.refresh(db_category)
    return ResponseHandler.update_success("Category", db_category.id, db_category)

def delete_category_by_id(db:Session, category_id: int):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
        return ResponseHandler.delete_success("Product", db_category.id, db_category)
    return ResponseHandler.single_not_found_error("Product", db_category.id)
