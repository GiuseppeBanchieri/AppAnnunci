from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher


password_hash = PasswordHash([Argon2Hasher()])

def hash_password(password: str) -> str:
  return password_hash.hash(password)

def verify_password(plaintext_password: str, hashed_password: str) -> bool:
  return password_hash.verify(plaintext_password, hashed_password)