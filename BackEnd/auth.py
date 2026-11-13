from datetime import UTC, datetime, timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'api/users/login')

class Password():

  password_hash = PasswordHash([Argon2Hasher()])

  @staticmethod
  def hash(password: str) -> str:
    return Password.password_hash.hash(password)

  @staticmethod
  def verify(plaintext_password: str, hashed_password: str) -> bool:
    return Password.password_hash.verify(plaintext_password, hashed_password)

class AccessToken():

  @staticmethod
  def create(data: dict, minutes_to_expiration: int = settings.access_token_expire_minutes) -> str:
    to_encode = data.copy()
    expiration_delta = datetime.now(UTC) + timedelta(minutes=minutes_to_expiration)
    to_encode.update({'expiration':expiration_delta})
    encoded_token = jwt.encode(to_encode, settings.secret_key.get_secret_value(), algorithm=settings.algorithm)
    return encoded_token

  @staticmethod
  def verify(token: str) -> str | None:
    try:
      payload = jwt.decode(
        token, settings.secret_key.get_secret_value(), algorithms=[settings.algorithm], options={'require': ['exp', 'sub']}
        )
    except jwt.InvalidTokenError:
      return None
    else:
      return payload.get('sub')

