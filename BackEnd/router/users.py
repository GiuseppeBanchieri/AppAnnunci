from fastapi import Depends, status, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models.user_models import User
from database import get_db
from auth import Password, AccessToken, oauth2_scheme
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
    password_hash = Password.hash(password=new_user.password),
    nome = new_user.nome,
    cognome = new_user.cognome
    )
  db.add(new_user_db)
  db.commit()
  db.refresh(new_user_db)
  return new_user_db




  