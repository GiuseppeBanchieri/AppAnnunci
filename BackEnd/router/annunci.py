from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Annotated

from database import get_db
from models.annuncio_models import Annuncio
from schemas.annuncio_schemas import AnnuncioResponse, AnnuncioCreate, AnnuncioPatch

router = APIRouter(
  prefix='/api/annunci',
  tags=['Annunci']
)


@router.get('/', response_model=List[AnnuncioResponse])
def get_all_annunci(db: Annotated[Session, Depends(get_db)]):
  annunci = db.scalars(select(Annuncio)).all()
  if annunci:
    return annunci
  raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Errore: Non sono presenti annunci nel DB')

@router.get('/{annuncio_id}', response_model=AnnuncioResponse)
def get_one_annuncio(annuncio_id: int, db: Annotated[Session, Depends(get_db)]):
  annuncio = db.scalars(select(Annuncio).where(Annuncio.id == annuncio_id)).first()
  if annuncio is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Errore: L\'annuncio selezionato non è presente nel DB')
  else:
    return annuncio

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=AnnuncioResponse)
def post_annuncio(annuncio: AnnuncioCreate, db: Annotated[Session, Depends(get_db)]):
  nuovo_annuncio = Annuncio(**annuncio.model_dump())
  db.add(nuovo_annuncio)
  db.commit()
  db.refresh(nuovo_annuncio)
  return nuovo_annuncio

@router.put('/{annuncio_id}', response_model=AnnuncioResponse)
def put_post(annuncio_id: int, annuncio_modificato: AnnuncioCreate, db: Annotated[Session, Depends(get_db)]):
  #Put crea una nuova risorsa o rimpiazza la risorsa identificata col contenuto della risposta, è un update completo
  annuncio = db.scalars(select(Annuncio).where(Annuncio.id == annuncio_id)).first()
  if annuncio is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Errore: L\'annuncio selezionato non è presente nel DB')
  update_data = annuncio_modificato.model_dump()
  for key, value in update_data.items():
    setattr(annuncio, key, value)
  db.commit()
  db.refresh(annuncio)
  return annuncio


@router.patch('/{annuncio_id}', response_model=AnnuncioResponse)
def put_post(annuncio_id: int, annuncio_modificato: AnnuncioPatch, db: Annotated[Session, Depends(get_db)]):
  #Patch è un update parziale
  annuncio = db.scalars(select(Annuncio).where(Annuncio.id == annuncio_id)).first()
  if annuncio is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Errore: L\'annuncio selezionato non è presente nel DB')

  update_data = annuncio_modificato.model_dump(exclude_unset=True, exclude_defaults=True)
  for key, value in update_data.items():
    setattr(annuncio, key, value)

  db.commit()
  db.refresh(annuncio)
  return annuncio

@router.delete('/{annuncio_id}', status_code=status.HTTP_204_NO_CONTENT)
def get_one_annuncio(annuncio_id: int, db: Annotated[Session, Depends(get_db)]):
  annuncio = db.scalars(select(Annuncio).where(Annuncio.id == annuncio_id)).first()
  if annuncio is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Errore: L\'annuncio selezionato non è presente nel DB')
  else:
    db.delete(annuncio)
    db.commit()