from fastapi import Depends, status, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, UTC

from models.user_models import User, PasswordResetToken
from database import get_db
from auth import password, jwt, pw_reset
from email_service.send_forgotten_pw_emails import send_forgotten_pw_email
from schemas.user_schemas import *
from config import settings


router = APIRouter(
  prefix='/api/users',
  tags=['Authentication']
)


@router.post('/', response_model=UserResponsePrivate, status_code=status.HTTP_201_CREATED)
async def create_user(new_user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):

  existing_user_query = await db.scalars(select(User).where(User.email == new_user.email))
  existing_user_db = existing_user_query.first()
  if existing_user_db:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email già registrata')
  
  new_user_db = User(
    email = new_user.email,
    password_hash = password.hash_password(password=new_user.password),
    nome = new_user.nome,
    cognome = new_user.cognome
    )
  
  db.add(new_user_db)
  await db.commit()
  await db.refresh(new_user_db)

  return new_user_db


@router.post('/login', response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[AsyncSession, Depends(get_db)]):
  #Il campo username del formdata, che deve essere chiamato così per essere conforme a OAuth2, è la mail

  user_query = await db.scalars(select(User).where(User.email == form_data.username))
  user = user_query.first()
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
async def get_current_user(current_user: Annotated[User, Depends(jwt.jwt_get_current_user)]):
  return current_user


@router.patch('/me/password', status_code=status.HTTP_200_OK)
async def cambio_password(password_data: ChangePasswordRequest, 
                          current_user: Annotated[User, Depends(jwt.jwt_get_current_user)], db: Annotated[AsyncSession, Depends(get_db)]):

  pw_verification = password.verify_password(password_data.current_password, current_user.password_hash)
  if not pw_verification or password_data.current_password == password_data.new_password:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Password vecchia non corretta o uguale a password nuova')
  else:
    current_user.password_hash = password.hash_password(password_data.new_password)
    await db.commit()


@router.patch('/{user_id}', response_model=UserResponsePrivate)
async def patch_user(user_id: int, user_modificato:UserPatch, db: Annotated[AsyncSession, Depends(get_db)],
               auth_id: Annotated[int, Depends(jwt.VerifyJWT(return_user_id=True))]):
  
  if user_id != auth_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Utente non autorizzato a modificare questo profilo')
  
  user_query = await db.scalars(select(User).where(User.id == user_id))
  user_db = user_query.first()
  if user_db is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Errore: Utente selezionato non è presente nel DB')
  
  update_data = user_modificato.model_dump(exclude_unset=True, exclude_defaults=True)
  #Controllo che la mail nuova, se è parte della modifica, non sia già in db, in quanto ha la restrizione unique
  nuova_email: str | None = update_data.get('email')
  if nuova_email is not None and nuova_email != user_db.email:
    user_esistente_nuova_mail_query = await db.scalars(select(User).where(User.email == nuova_email))
    user_esistente_nuova_mail = user_esistente_nuova_mail_query.first()
    if user_esistente_nuova_mail is not None:
      raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Indirizzo mail è già assegnato ad un utente')
  for key, attr in update_data.items():
    setattr(user_db, key, attr)
  
  await db.commit()
  await db.refresh(user_db)

  return user_db
  

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Annotated[AsyncSession, Depends(get_db)],
                auth_id: Annotated[int, Depends(jwt.VerifyJWT(return_user_id=True))]):
  
  if user_id != auth_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Utente non autorizzato a cancellare questo profilo')
  user_query = await db.scalars(select(User).where(User.id == user_id))
  user_db = user_query.first()
  if user_db is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Utente selezionato non è presente nel DB')
  else:
    await db.delete(user_db)
    await db.commit()


@router.post('/password_dimenticata', status_code=status.HTTP_202_ACCEPTED)
async def password_dimenticata(request_data: ForgotPasswordRequest, db: Annotated[AsyncSession, Depends(get_db)]):
#Chiamato quando si è dimenticata la password per mandare mail con link di recupero

  user_query = await db.scalars(select(User).where(User.email == request_data.email))
  user_db = user_query.first()
  if user_db is None:
    #non ritorniamo un 404 perchè non vogliamo far sapere a quali utenti sono nel db
    return
  else: 
    await db.execute(delete(PasswordResetToken).where(PasswordResetToken.user_id == user_db.id))
    token = pw_reset.generate_reset_token()
    hashed_token = pw_reset.hash_reset_token(token)
    scadenza = datetime.now(UTC) + timedelta(minutes=settings.password_reset_token_expiration_minutes)
    reset_token_db = PasswordResetToken(token_hash=hashed_token,
                                     scadenza=scadenza,
                                     user_id=user_db.id)
    db.add(reset_token_db)
    await db.commit()
    await send_forgotten_pw_email(mail_recipient=user_db.email,
                                  nome_user=user_db.nome,
                                  token=token)


@router.post('/password_reset', status_code=status.HTTP_200_OK)
async def reset_password(request_data: ResetPasswordRequest, db: Annotated[AsyncSession, Depends(get_db)]):
#Chiamato dalla pagina di recupero della password linkata nella mail

  request_token_hash = pw_reset.hash_reset_token(request_data.token)
  token_query = await db.scalars(select(PasswordResetToken).where(PasswordResetToken.token_hash == request_token_hash))
  token_db = token_query.first()

  if token_db is None:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Token non valido o scaduto')
  if token_db.scadenza < datetime.now(UTC):
    await db.delete(token_db)
    await db.commit()
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Token non valido o scaduto')

  user_query = await db.scalars(select(User).where(User.id == token_db.user_id))
  user_db = user_query.first()
  if user_db is None:
    await db.delete(token_db)
    await db.commit()
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Token non valido o scaduto')

  user_db.password_hash = password.hash_password(request_data.new_password)

  await db.execute(delete(PasswordResetToken).where(PasswordResetToken.user_id == user_db.id))
  await db.commit()