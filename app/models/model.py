from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from pydantic import BaseModel
from typing import Optional

SQLALCHEMY_DATABASE_URL = "sqlite:///./loja.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=True)
    address = Column(String, nullable=True)

class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    card_name = Column(String, nullable=False)
    card_number = Column(String, nullable=False)
    cvv = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    card_type = Column(String, nullable=False)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, nullable=False)
    product_title = Column(String, nullable=False)
    total_price = Column(Float, nullable=False)

class UserCreate(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    username: str
    email: Optional[str] = None
    address: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    address: Optional[str] = None
    class Config:
        from_attributes = True

class PaymentCreate(BaseModel):
    card_name: str
    card_number: str
    cvv: str
    brand: str
    card_type: str

class PaymentResponse(BaseModel):
    id: int
    card_name: str
    card_number: str
    brand: str
    card_type: str

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    product_id: int
    product_title: str
    total_price: float

class OrderResponse(BaseModel):
    id: int
    product_id: int
    product_title: str
    total_price: float
    class Config:
        from_attributes = True