from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, UTC

from database import Base

class User(Base):
  __tablename__ = 'users'

  id: Mapped[int] = mapped_column(primary_key=True)
  email: Mapped[str] = mapped_column(String(200), unique=True, index=True)
  password_hash: Mapped[str] = mapped_column(String(200))
  nome: Mapped[str] = mapped_column(String(100))
  cognome: Mapped[str | None] = mapped_column(String(100), nullable=True)


class PasswordResetToken(Base):
  __tablename__ = 'password_reset_tokens'

  id: Mapped[int] = mapped_column(primary_key=True)
  token_hash: Mapped[str] = mapped_column(String(64), unique=True)
  scadenza: Mapped[datetime] = mapped_column(DateTime(timezone=True))
  creazione: Mapped[datetime] = mapped_column(DateTime(timezone=True), default= lambda: datetime.now(UTC))
  user_id = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
