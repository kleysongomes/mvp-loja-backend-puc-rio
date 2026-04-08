from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.model import (
    User, UserCreate, UserUpdate, UserResponse, 
    PaymentMethod, PaymentCreate, PaymentResponse,
    Order, OrderCreate, OrderResponse, get_db
)
import bcrypt
import jwt
import requests
from datetime import datetime, timedelta

router = APIRouter()
SECRET_KEY = "chave_secreta_super_segura_do_mvp"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_password_hash(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username já registrado")
    new_user = User(username=user.username, password=get_password_hash(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    expire = datetime.utcnow() + timedelta(minutes=60)
    token = jwt.encode({"sub": db_user.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/users/me", response_model=UserResponse)
def update_user_me(user_update: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.username = user_update.username
    current_user.email = user_update.email
    current_user.address = user_update.address
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.delete(current_user)
    db.commit()
    return {"mensagem": "Conta deletada"}

@router.post("/payments/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(payment: PaymentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_payment = PaymentMethod(
        user_id=current_user.id, card_name=payment.card_name, card_number=payment.card_number, 
        cvv=payment.cvv, brand=payment.brand, card_type=payment.card_type
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@router.get("/payments/", response_model=list[PaymentResponse])
def get_payments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(PaymentMethod).filter(PaymentMethod.user_id == current_user.id).all()

@router.delete("/payments/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(payment_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    payment = db.query(PaymentMethod).filter(PaymentMethod.id == payment_id, PaymentMethod.user_id == current_user.id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    db.delete(payment)
    db.commit()
    return {"mensagem": "Cartão deletado"}

@router.post("/orders/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_order = Order(user_id=current_user.id, product_id=order.product_id, product_title=order.product_title, total_price=order.total_price)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@router.get("/orders/", response_model=list[OrderResponse])
def get_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Order).filter(Order.user_id == current_user.id).all()

@router.get("/produtos/")
def listar_produtos():
    response = requests.get("https://fakestoreapi.com/products")
    return {"produtos": response.json()}

@router.get("/produtos/{produto_id}")
def buscar_produto(produto_id: int):
    response = requests.get(f"https://fakestoreapi.com/products/{produto_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return response.json()