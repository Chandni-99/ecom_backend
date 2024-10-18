import uuid
from sqlalchemy import Column, Integer, TIMESTAMP, String, Float, Double, ForeignKey, text, Numeric, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
from app.db.base_class import Base


class BaseClass(Base):
    __abstract__ = True  # This class should not be instantiated directly
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)  # Nullable for soft delete


class User(BaseClass):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    uuid = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()), nullable=False)
    username = Column(String(255), index=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, server_default=expression.true(), nullable=False)

    # Relationships
    cart = relationship("Cart", back_populates="user")  # Correctly referenced relationship
    reviews = relationship("Review", back_populates="user")  # Correctly referenced relationship


class Admin(BaseClass):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    username = Column(String(255), index=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)


class Product(BaseClass):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    discount_percentage = Column(Integer, default=0, nullable=False)
    brand = Column(String(255), nullable=False)
    image_url = Column(String(512))  # Store the image URL

    # Relationships
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    category = relationship("Category", back_populates="products")  # Correctly referenced relationship
    reviews = relationship("Review", back_populates="product")  # Correctly referenced relationship


class Category(BaseClass):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    name = Column(String(255), unique=True, nullable=False)

    # Relationships
    products = relationship("Product", back_populates="category")  # Correctly referenced relationship


class Cart(BaseClass):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    total_amount = Column(Double, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="cart")  # Correctly referenced relationship
    items = relationship("CartItem", back_populates="cart")  # Correctly referenced relationship


class CartItem(BaseClass):
    __tablename__ = "cartitems"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    cart = relationship("Cart", back_populates="items")  # Correctly referenced relationship
    product = relationship("Product")  # No back_populates needed here


class Review(BaseClass):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    rating = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="reviews")  # Correctly referenced relationship
    product = relationship("Product", back_populates="reviews")  # Correctly referenced relationship
