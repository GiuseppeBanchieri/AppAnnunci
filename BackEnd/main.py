from fastapi import FastAPI

from database import engine, Base
from router import annunci, users


app = FastAPI()
app.include_router(annunci.router)
app.include_router(users.router)

Base.metadata.create_all(engine)

@app.get('/api')
def example():
  return {'text': 'hello world'}
