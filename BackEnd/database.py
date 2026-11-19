from config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(expire_on_commit=False, bind=engine, class_= AsyncSession)

class Base(DeclarativeBase):
  pass

async def get_db():
  async with AsyncSessionLocal() as session:
    yield session