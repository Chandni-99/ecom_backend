from fastapi import APIRouter

from app.core.security import get_current_user

router = APIRouter(tags=["Carts"], prefix="/carts")

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.crud.carts import create_cart, get_cart, get_carts, update_cart, delete_cart
from app.schemas.carts import CartCreate, CartUpdate, CartOut, CartsOut, CartOutDelete
from app.db.base_class import get_db  # Assuming you have a method to get the DB session
from app.models.models import User  # Assuming you have a User model and an auth dependency


router = APIRouter(tags=["Carts"], prefix="/carts", dependencies=[Depends(get_current_user)])

# Create a cart
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CartOut)
async def create_cart_route(
    cart: CartCreate,
    db: Session = Depends(get_db)  # Assuming you have a current user dependency
):
    return create_cart(db, cart)


# Get a single cart
@router.get("/{cart_id}", status_code=status.HTTP_200_OK, response_model=CartOut)
async def get_cart_route(
    cart_id: int,
    db: Session = Depends(get_db),
):
    return get_cart(db, cart_id)


# Get all carts for a user
@router.get("/user/", status_code=status.HTTP_200_OK, response_model=CartsOut)
async def get_carts_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # Assuming you have a current user dependency
):
    return get_carts(db, user_id=current_user.id)


# Update a cart
@router.put("/{cart_id}", status_code=status.HTTP_200_OK, response_model=CartOut)
async def update_cart_route(
    cart_id: int,
    cart_data: CartUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_cart(db, cart_id, cart_data, user_id=current_user.id)


# Delete a cart
@router.delete("/{cart_id}", status_code=status.HTTP_200_OK, response_model=CartOutDelete)
async def delete_cart_route(
    cart_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_cart(db, cart_id, user_id=current_user.id)
