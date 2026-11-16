from datetime import UTC, datetime, timedelta
from fastapi import HTTPException, status, Depends
import jwt
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session

from config import settings
from models.user_models import User
from database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'api/users/login')

def jwt_create(data: dict, minutes_to_expiration: int = settings.access_token_expire_minutes) -> str:
  to_encode = data.copy()
  expiration_delta = datetime.now(UTC) + timedelta(minutes=minutes_to_expiration)
  to_encode.update({'exp':expiration_delta})
  encoded_token = jwt.encode(to_encode, settings.secret_key.get_secret_value(), algorithm=settings.algorithm)
  return encoded_token

def jwt_verify(token: Annotated[str, Depends(oauth2_scheme)]) ->  None:
  try:
    jwt.decode(
      token, settings.secret_key.get_secret_value(), algorithms=[settings.algorithm], options={'require': ['exp', 'sub']}
      )
  except jwt.InvalidTokenError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='JWT scaduto o non valido', headers={'WWW-Authenticate':'Bearer'})
  else:
    return None
  
def jwt_get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)]) -> int:
  try:
    payload = jwt.decode(
      token, settings.secret_key.get_secret_value(), algorithms=[settings.algorithm], options={'require': ['exp', 'sub']}
      )
  except jwt.InvalidTokenError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='JWT scaduto o non valido', headers={'WWW-Authenticate':'Bearer'})
  else:
    user_id = payload.get('sub')
    if user_id == None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='JWT scaduto o non valido', headers={'WWW-Authenticate':'Bearer'})
    else:
      return int(user_id)

def jwt_get_current_user(user_id: Annotated[int, Depends(jwt_get_current_user_id)], db: Annotated[Session, Depends(get_db)]) -> User:
  user = db.scalars(select(User).where(User.id == user_id)).first()
  if user == None: 
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='JWT scaduto o non valido', headers={'WWW-Authenticate':'Bearer'})
  else:
    return user

  