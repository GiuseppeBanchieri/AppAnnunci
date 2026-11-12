from pydantic import BaseModel, Field
from datetime import datetime

class AnnuncioSampleData(BaseModel):
  id: int
  codice_lingua_id: int | None
  titolo: str = Field(min_length=1, max_length=100)
  contenuto: str | None
  pubblicato: bool | None
  categoria_id: int | None
  sub_categoria_id: int | None
  tipo_contratto_id: int | None
  monte_ore_id: int | None
  smart_working: bool | None
  job_title: str = Field(min_length=1, max_length=100)
  salario_min: int | None
  salario_max: int | None
  codice_valuta_id: int | None
  unita_erogazione_salario_id: int | None
  datetime_pubblicazione : datetime | None
  datetime_chiusura : datetime | None
  regione_id: int | None
  citta_id: int | None
  formazione_id: int | None