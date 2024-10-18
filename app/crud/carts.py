from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.models import Cart  # Assuming you have a Cart model defined
from app.schemas.carts import CartCreate, CartUpdate
from app.utils.responses import ResponseHandler


def create_cart(db: Session, cart: CartCreate):
    try:
        db_cart = Cart(**cart.dict())
        db.add(db_cart)
        db.commit()
        db.refresh(db_cart)
        return ResponseHandler.create_success("Cart", db_cart.id, db_cart)
    except IntegrityError as e:
        db.rollback()
        # return ResponseHandler.error(f"Failed to create cart: {str(e)}")


def get_cart(db: Session, cart_id: int):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        return ResponseHandler.single_not_found_error("Cart", cart_id)
    return ResponseHandler.get_single_success("Cart", cart.id, cart)


def get_carts(db: Session, user_id: int):
    carts = db.query(Cart).filter(Cart.user_id == user_id).all()
    if not carts:
        return ResponseHandler.not_found_error("Carts for this user")
    return ResponseHandler.success(f"Carts for user with id {user_id}", carts)


def update_cart(db: Session, cart_id: int, cart_data: CartUpdate, user_id: int):
    cart = db.query(Cart).filter(Cart.id == cart_id, Cart.user_id == user_id).first()
    if not cart:
        return ResponseHandler.single_not_found_error("Cart", cart_id)

    for key, value in cart_data.dict().items():
        setattr(cart, key, value)
    db.commit()
    db.refresh(cart)
    return ResponseHandler.update_success("Cart", cart.id, cart)


def delete_cart(db: Session, cart_id: int, user_id: int):
    cart = db.query(Cart).filter(Cart.id == cart_id, Cart.user_id == user_id).first()
    if not cart:
        return ResponseHandler.single_not_found_error("Cart", cart_id)

    db.delete(cart)
    db.commit()
    return ResponseHandler.delete_success("Cart", cart.id)
