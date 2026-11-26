from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import engine, Base
from router import annunci, users


@asynccontextmanager
async def lifespan(_app: FastAPI):
  """  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)"""
  yield
  await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(annunci.router)
app.include_router(users.router)

@app.get('/api')
def example():
  return {'text': 'hello world'}
