from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class ListaAnnunciPaginata(BaseModel):
  annunci: list[AnnuncioResponse]
  tot_annunci: int
  offset: int
  limit: int
  tot_pagine: int
  pag_corrente: int
  has_more: bool

class AnnuncioBase(BaseModel):
  titolo: str = Field(min_length=1, max_length=100)
  contenuto: str | None = Field(default= None)
  pubblicato: bool | None = Field(default= None)
  smart_working: bool | None = Field(default= None)
  job_title: str = Field(min_length=1, max_length=100)
  salario_min: int | None = Field(default= None)
  salario_max: int | None = Field(default= None)
  datetime_pubblicazione : datetime | None = Field(default= None)
  datetime_chiusura : datetime | None = Field(default= None)


class AnnuncioCreate(AnnuncioBase):
  codice_lingua_id: int | None = Field(default= None)
  categoria_id: int | None = Field(default= None)
  sub_categoria_id: int | None = Field(default= None)
  tipo_contratto_id: int | None = Field(default= None)
  monte_ore_id: int | None = Field(default= None)
  codice_valuta_id: int | None = Field(default= None)
  unita_erogazione_salario_id: int | None = Field(default= None)
  regione_id: int | None = Field(default= None)
  citta_id: int | None = Field(default= None)
  formazione_id: int | None = Field(default= None)

class AnnuncioPatch(AnnuncioCreate):
  #Non deve avere campi obbligatori, Patch è un update parziale, per questo aggiorno gli unici due che lo erano
  job_title: str | None = Field(default = None, min_length=1, max_length=100)
  titolo: str | None = Field(default = None, min_length=1, max_length=100)


class AnnuncioResponse(AnnuncioBase):
  id: int
  codice_lingua: CodiceLinguaResponse | None = Field(default= None)
  categoria: CategoriaResponse | None = Field(default= None)
  sub_categoria: SubCategoriaResponse | None = Field(default= None)
  tipo_contratto: TipoContrattoResponse | None = Field(default= None)
  monte_ore: MonteOreResponse | None = Field(default= None)
  codice_valuta: CodiceValutaResponse | None = Field(default= None)
  unita_erogazione_salario: UnitaErogazioneSalarioResponse | None = Field(default= None)
  regione: RegioneResponse | None = Field(default= None)
  citta: CittaResponse | None = Field(default= None)
  formazione: FormazioneResponse | None = Field(default= None)

  model_config = ConfigDict(from_attributes=True)


class CodiceLinguaResponse(BaseModel):
  id: int | None = Field(default= None)
  codice: str | None = Field(default= None)
  model_config = ConfigDict(from_attributes=True)

class CategoriaResponse(BaseModel):
  id: int | None = Field(default= None)
  categoria: str | None = Field(default= None)
  model_config = ConfigDict(from_attributes=True)

class SubCategoriaResponse(BaseModel):
  id: int | None = Field(default= None)
  sub_categoria: str | None = Field(default= None)
  model_config = ConfigDict(from_attributes=True)

class TipoContrattoResponse(BaseModel):
  id: int | None = Field(default= None)
  tipo: str | None = Field(default= None)
  model_config = ConfigDict(from_attributes=True)

class MonteOreResponse(BaseModel):
  id: int | None = Field(default= None)
  monte_ore: str | None = Field(default= None)
  model_config = ConfigDict(from_attributes=True)
  
class CodiceValutaResponse(BaseModel):
  id: int | None = Field(default= None)
  codice: str | None = Field(default= None)
  model_config = ConfigDict(from_attributes=True)
  
class UnitaErogazioneSalarioResponse(BaseModel):
  id: int | None = Field(default= None)
  unita: str | None = Field(default= None)
  model_config = ConfigDict(from_attributes=True)
  
class RegioneResponse(BaseModel):
  id: int | None = Field(default= None)
  regione: str | None = Field(default= None)
  model_config = ConfigDict(from_attributes=True)
  
class CittaResponse(BaseModel):
  id: int | None = Field(default= None)
  citta: str | None = Field(default= None)
  model_config = ConfigDict(from_attributes=True)
  
class FormazioneResponse(BaseModel):
  id: int | None = Field(default= None)
  titolo: str | None = Field(default= None)
  model_config = ConfigDict(from_attributes=True)
  