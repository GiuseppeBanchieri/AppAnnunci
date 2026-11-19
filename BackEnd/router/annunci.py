from fastapi import Depends, status, APIRouter, HTTPException, Query
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, table, column
from typing import Annotated
from math import ceil

from database import get_db
from models.annuncio_models import Annuncio
from schemas.annuncio_schemas import AnnuncioResponse, AnnuncioCreate, AnnuncioPatch, ListaAnnunciPaginata
from auth import jwt

router = APIRouter(
  prefix='/api/annunci',
  tags=['Annunci']
)


@router.get('/', response_model=ListaAnnunciPaginata)
async def get_all_annunci(db: Annotated[AsyncSession, Depends(get_db)],
                    ofs: Annotated[int, Query(ge=0, description='Numero di elementi da saltare per la paginazione, deve essere maggiore o uguale a 0, default è 0')] = 0,
                    lim: Annotated[int, Query(ge=1, le=50, description='Numero di elementi da ritornare per ogni pagina, deve essere uguale o inferiore a 50, default è 50')] = 50
                    ):
  
  annunci_query = await db.scalars(select(Annuncio).options(
    selectinload(Annuncio.codice_lingua), selectinload(Annuncio.categoria), selectinload(Annuncio.sub_categoria), selectinload(Annuncio.tipo_contratto), selectinload(Annuncio.monte_ore), selectinload(Annuncio.codice_valuta), selectinload(Annuncio.unita_erogazione_salario), selectinload(Annuncio.regione), selectinload(Annuncio.citta), selectinload(Annuncio.formazione)
    ).order_by(Annuncio.datetime_pubblicazione.desc()).limit(lim).offset(ofs))
  annunci = annunci_query.all()
  if len(annunci) == 0:
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Errore: Non sono presenti annunci nel DB')
  tot_ann = await db.scalar(select(func.count()).select_from(table(Annuncio.__tablename__, column('id'))))
  tot_pag = ceil(tot_ann / lim)
  pag_corr = ceil((ofs / lim) +1)
  has_more = ofs + len(annunci) < tot_ann
  return ListaAnnunciPaginata(annunci= [AnnuncioResponse.model_validate(annuncio) for annuncio in annunci],
                              offset=ofs,
                              limit=lim,
                              tot_annunci=tot_ann,
                              tot_pagine=tot_pag,
                              pag_corrente=pag_corr,
                              has_more=has_more)
  

@router.get('/{annuncio_id}', response_model=AnnuncioResponse)
async def get_one_annuncio(annuncio_id: int, db: Annotated[AsyncSession, Depends(get_db)],
                     auth: Annotated[None, Depends(jwt.VerifyJWT(return_user_id=False))]):
  
  annuncio_query = await db.scalars(select(Annuncio).options(
    selectinload(Annuncio.codice_lingua), selectinload(Annuncio.categoria), selectinload(Annuncio.sub_categoria), selectinload(Annuncio.tipo_contratto), selectinload(Annuncio.monte_ore), selectinload(Annuncio.codice_valuta), selectinload(Annuncio.unita_erogazione_salario), selectinload(Annuncio.regione), selectinload(Annuncio.citta), selectinload(Annuncio.formazione)
    ).where(Annuncio.id == annuncio_id))
  annuncio = annuncio_query.first()
  if annuncio is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Errore: L\'annuncio selezionato non è presente nel DB')
  else:
    return annuncio


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=AnnuncioResponse)
async def post_annuncio(nuovo_annuncio: AnnuncioCreate, db: Annotated[AsyncSession, Depends(get_db)],
                  auth: Annotated[None, Depends(jwt.VerifyJWT(return_user_id=False))]):
  
  nuovo_annuncio_db = Annuncio(**nuovo_annuncio.model_dump())
  db.add(nuovo_annuncio_db)
  await db.commit()
  await db.refresh(nuovo_annuncio_db, attribute_names=['codice_lingua', 'categoria', 'sub_categoria', 'tipo_contratto', 'monte_ore', 'codice_valuta', 'unita_erogazione_salario', 'regione', 'citta', 'formazione'])
  return nuovo_annuncio_db


@router.put('/{annuncio_id}', response_model=AnnuncioResponse)
async def put_post(annuncio_id: int, annuncio_modificato: AnnuncioCreate, db: Annotated[AsyncSession, Depends(get_db)],
             auth: Annotated[None, Depends(jwt.VerifyJWT(return_user_id=False))]):
  
  #Put crea una nuova risorsa o rimpiazza la risorsa identificata col contenuto della risposta, è un update completo
  annuncio_query = await db.scalars(select(Annuncio).where(Annuncio.id == annuncio_id))
  annuncio = annuncio_query.first()
  if annuncio is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Errore: L\'annuncio selezionato non è presente nel DB')
  update_data = annuncio_modificato.model_dump()
  for key, value in update_data.items():
    setattr(annuncio, key, value)
  await db.commit()
  await db.refresh(annuncio, attribute_names=['codice_lingua', 'categoria', 'sub_categoria', 'tipo_contratto', 'monte_ore', 'codice_valuta', 'unita_erogazione_salario', 'regione', 'citta', 'formazione'])
  return annuncio


@router.patch('/{annuncio_id}', response_model=AnnuncioResponse)
async def patch_post(annuncio_id: int, annuncio_modificato: AnnuncioPatch, db: Annotated[AsyncSession, Depends(get_db)],
             auth: Annotated[None, Depends(jwt.VerifyJWT(return_user_id=False))]):
  
  #Patch è un update parziale
  annuncio_query = await db.scalars(select(Annuncio).where(Annuncio.id == annuncio_id))
  annuncio = annuncio_query.first()
  if annuncio is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Errore: L\'annuncio selezionato non è presente nel DB')

  update_data = annuncio_modificato.model_dump(exclude_unset=True)
  for key, value in update_data.items():
    setattr(annuncio, key, value)

  await db.commit()
  await db.refresh(annuncio, attribute_names=['codice_lingua', 'categoria', 'sub_categoria', 'tipo_contratto', 'monte_ore', 'codice_valuta', 'unita_erogazione_salario', 'regione', 'citta', 'formazione'])
  return annuncio


@router.delete('/{annuncio_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_annuncio(annuncio_id: int, db: Annotated[AsyncSession, Depends(get_db)],
                     auth: Annotated[None, Depends(jwt.VerifyJWT(return_user_id=False))]):

  annuncio_query = await db.scalars(select(Annuncio).where(Annuncio.id == annuncio_id))
  annuncio = annuncio_query.first()
  if annuncio is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Errore: L\'annuncio selezionato non è presente nel DB')
  else:
    await db.delete(annuncio)
    await db.commit()