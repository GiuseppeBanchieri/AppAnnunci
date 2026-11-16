from fastapi import Depends, status, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models.user_models import User
from database import get_db
from auth import password, jwt
from schemas.user_schemas import *


router = APIRouter(
  prefix='/api/users',
  tags=['Authentication']
)


@router.post('/', response_model=UserResponsePrivate, status_code=status.HTTP_201_CREATED)
def create_user(new_user: UserCreate, db: Annotated[Session, Depends(get_db)]):
  existing_user_db = db.scalars(select(User).where(User.email == new_user.email)).first()
  if existing_user_db:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email già registrata')
  new_user_db = User(
    email = new_user.email,
    password_hash = password.hash_password(password=new_user.password),
    nome = new_user.nome,
    cognome = new_user.cognome
    )
  db.add(new_user_db)
  db.commit()
  db.refresh(new_user_db)
  return new_user_db

@router.post('/login', response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
  #Il campo username del formdata, che deve essere chiamato così per essere conforme a OAuth2, è la mail
  user = db.scalars(select(User).where(User.email == form_data.username)).first()
  password_verification = False
  if user:
    password_verification = password.verify_password(form_data.password, user.password_hash)

  if password_verification == False:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Email o password non corrette', headers={'WWW-Authenticate':'Bearer'})

  return Token(
    acces_token=jwt.jwt_create(data={'sub': str(user.id)}),
    type='bearer'
    )

@router.get('/me', response_model=UserResponsePrivate)
def get_current_user(current_user: Annotated[User, Depends(jwt.jwt_get_current_user)]):
  return current_user