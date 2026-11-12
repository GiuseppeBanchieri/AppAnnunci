from fastapi import FastAPI

from database import engine, Base
from router import annunci


app = FastAPI()
app.include_router(annunci.router)

Base.metadata.create_all(engine)

@app.get('/api')
def example():
  return {'text': 'hello world'}
