import asyncio
import json
from sqlalchemy import select
from datetime import datetime
from typing import List, Dict
import re

from database import AsyncSessionLocal
from models import annuncio_models as models
from schemas.sample_data_schema import AnnuncioSampleData


db = AsyncSessionLocal()
sample_data_path = './test_data/job_postings_2000.json'



def load_data(path: str) -> List[Dict]:
  with open(path, 'r', encoding='utf-8') as file:
    data: List[Dict] = json.load(file)
    return data

def sanitize_string_input(string_input: str) -> str:
  #funzione per sanitizzare l'input str di metadati che devono essere unique. Questa sanitizzazione serve solo ad avere un formatting consistente per questi valori.
  return re.sub(r'\s+', ' ', string_input.strip().lower())

async def insert_sample_annuncio(annuncio: AnnuncioSampleData) -> None:

  query_annuncio = await db.scalars(select(models.Annuncio.id).where(models.Annuncio.id == annuncio.id))
  annuncio_db = query_annuncio.first()
  if annuncio_db is None:
    nuovo_annuncio_db = models.Annuncio(**annuncio.model_dump())
    db.add(nuovo_annuncio_db)
    await db.flush()


async def insert_sample_data(data: list) -> None:
  for row in data:
    nuovo_annuncio_id: int = row['id']

    nuovo_codice_lingua = sanitize_string_input(row['languageCode'])
    codice_lingua_id_query = await db.scalars(select(models.CodiceLingua.id).where(models.CodiceLingua.codice == nuovo_codice_lingua))
    codice_lingua_id: int | None = codice_lingua_id_query.first()
    if codice_lingua_id is None:
      print('Inserimento nuovo codice lingua')
      nuovo_codice_lingua_db = models.CodiceLingua(codice = nuovo_codice_lingua)
      db.add(nuovo_codice_lingua_db)
      await db.flush()
      nuovo_codice_lingua = nuovo_codice_lingua_db.id
    else:
      nuovo_codice_lingua = codice_lingua_id

    nuovo_titolo: str = row['title']
    nuovo_contenuto: str = row['description']
    nuovo_pubblicato: bool = row['isPublished']

    nuova_categoria = sanitize_string_input(row['jobClassification']['category'])
    categoria_id_query = await db.scalars(select(models.Categoria.id).where(models.Categoria.categoria == nuova_categoria))
    categoria_id: int | None = categoria_id_query.first()
    if categoria_id is None:
      print('Inserimento nuova categoria')
      nuova_categoria_db = models.Categoria(categoria = nuova_categoria)
      db.add(nuova_categoria_db)
      await db.flush()
      nuova_categoria = nuova_categoria_db.id
    else:
      nuova_categoria = categoria_id

    nuova_sub_categoria = sanitize_string_input(row['jobClassification']['subCategory'])
    sub_categoria_id_query = await db.scalars(select(models.SubCategoria.id).where(models.SubCategoria.sub_categoria == nuova_sub_categoria))
    sub_categoria_id: int | None = sub_categoria_id_query.first()
    if sub_categoria_id is None:
      print('Inserimento nuova sub categoria')
      nuova_sub_categoria_db = models.SubCategoria(sub_categoria = nuova_sub_categoria, categorie_id = nuova_categoria)
      db.add(nuova_sub_categoria_db)
      await db.flush()
      nuova_sub_categoria = nuova_sub_categoria_db.id
    else:
      nuova_sub_categoria = sub_categoria_id

    nuovo_tipo_contratto = sanitize_string_input(row['jobInformation']['jobTypes'][0])
    tipo_contratto_id_query = await db.scalars(select(models.TipoContratto.id).where(models.TipoContratto.tipo == nuovo_tipo_contratto))
    tipo_contratto_id: int | None = tipo_contratto_id_query.first()
    if tipo_contratto_id is None:
      print('Inserimento nuovo tipo contratto')
      nuovo_tipo_contratto_db = models.TipoContratto(tipo = nuovo_tipo_contratto)
      db.add(nuovo_tipo_contratto_db)
      await db.flush()
      nuovo_tipo_contratto = nuovo_tipo_contratto_db.id
    else:
      nuovo_tipo_contratto = tipo_contratto_id

    nuovo_monte_ore = sanitize_string_input(row['jobInformation']['expectedHoursOfService'])
    monte_ore_id_query = await db.scalars(select(models.MonteOre.id).where(models.MonteOre.monte_ore == nuovo_monte_ore))
    monte_ore_id: int | None = monte_ore_id_query.first()
    if monte_ore_id is None:
      print('Inserimento nuovo monte ore')
      nuovo_monte_ore_db = models.MonteOre(monte_ore = nuovo_monte_ore)
      db.add(nuovo_monte_ore_db)
      await db.flush()
      nuovo_monte_ore = nuovo_monte_ore_db.id
    else:
      nuovo_monte_ore = monte_ore_id

    nuovo_smart_working: bool = row['jobInformation']['remoteWorkAllowed']
    nuovo_job_title: str = sanitize_string_input(row['jobTitle'])
    nuovo_salario_min: int = row['payRates']['salaryMin']
    nuovo_salario_max: int = row['payRates']['salaryMax']

    nuovo_codice_valuta = sanitize_string_input(row['payRates']['currencyCode'])
    codice_valuta_id_query = await db.scalars(select(models.CodiceValuta.id).where(models.CodiceValuta.codice == nuovo_codice_valuta))
    codice_valuta_id: int | None = codice_valuta_id_query.first()
    if codice_valuta_id is None:
      print('Inserimento nuovo codice valuta')
      nuovo_codice_valuta_db = models.CodiceValuta(codice = nuovo_codice_valuta)
      db.add(nuovo_codice_valuta_db)
      await db.flush()
      nuovo_codice_valuta = nuovo_codice_valuta_db.id
    else:
      nuovo_codice_valuta = codice_valuta_id

    nuova_unita_erogazione_salario = sanitize_string_input(row['payRates']['unit'])
    unita_erogazione_salario_id_query = await db.scalars(select(models.UnitaErogazioneSalario.id).where(models.UnitaErogazioneSalario.unita == nuova_unita_erogazione_salario))
    unita_erogazione_salario_id: int | None = unita_erogazione_salario_id_query.first()
    if unita_erogazione_salario_id is None:
      print('Inserimento nuova unita erogazione salario')
      nuova_unita_erogazione_salario_db = models.UnitaErogazioneSalario(unita = nuova_unita_erogazione_salario)
      db.add(nuova_unita_erogazione_salario_db)
      await db.flush()
      nuova_unita_erogazione_salario = nuova_unita_erogazione_salario_db.id
    else:
      nuova_unita_erogazione_salario = unita_erogazione_salario_id

    nuovo_datetime_pubblicazione: datetime = row['postingDetail']['postingTime']
    nuovo_datetime_chiusura : datetime | None = row['postingDetail']['closingTime']

    nuova_regione = sanitize_string_input(row['workLocationAddress']['administrativeArea'])
    regione_id_query = await db.scalars(select(models.Regione.id).where(models.Regione.regione == nuova_regione))
    regione_id: int | None = regione_id_query.first()
    if regione_id is None:
      print('Inserimento di una nuova regione')
      nuova_regione_db = models.Regione(regione = nuova_regione)
      db.add(nuova_regione_db)
      await db.flush()
      nuova_regione = nuova_regione_db.id
    else:
      nuova_regione = regione_id

    nuova_citta = sanitize_string_input(row['workLocationAddress']['locality'])
    citta_id_query = await db.scalars(select(models.Citta.id).where(models.Citta.citta == nuova_citta))
    citta_id: int | None = citta_id_query.first()
    if citta_id is None:
      print('Inserimento nuova città')
      nuova_citta_db = models.Citta(citta = nuova_citta, regione_id = nuova_regione)
      db.add(nuova_citta_db)
      await db.flush()
      nuova_citta = nuova_citta_db.id
    else:
      nuova_citta = citta_id

    nuova_formazione = sanitize_string_input(row['education']['degree'])
    formazione_id_query = await db.scalars(select(models.Formazione.id).where(models.Formazione.titolo == nuova_formazione))
    formazione_id: int | None = formazione_id_query.first()
    if formazione_id is None:
      print('Inserimento nuova formazione')
      nuova_formazione_db = models.Formazione(titolo = nuova_formazione)
      db.add(nuova_formazione_db)
      await db.flush()
      nuova_formazione = nuova_formazione_db.id
    else:
      nuova_formazione = formazione_id

    #Comporre il modello con i dati estratti
    nuovo_annuncio = AnnuncioSampleData(id=nuovo_annuncio_id,
                                        codice_lingua_id=nuovo_codice_lingua,
                                        titolo=nuovo_titolo,
                                        contenuto=nuovo_contenuto,
                                        pubblicato=nuovo_pubblicato,
                                        categoria_id=nuova_categoria,
                                        sub_categoria_id=nuova_sub_categoria,
                                        tipo_contratto_id=nuovo_tipo_contratto,
                                        monte_ore_id=nuovo_monte_ore,
                                        smart_working=nuovo_smart_working,
                                        job_title=nuovo_job_title,
                                        salario_min=nuovo_salario_min,
                                        salario_max=nuovo_salario_max,
                                        codice_valuta_id=nuovo_codice_valuta,
                                        unita_erogazione_salario_id=nuova_unita_erogazione_salario,
                                        datetime_pubblicazione=nuovo_datetime_pubblicazione,
                                        datetime_chiusura=nuovo_datetime_chiusura,
                                        regione_id=nuova_regione,
                                        citta_id=nuova_citta,
                                        formazione_id=nuova_formazione
                                        )
    
    await insert_sample_annuncio(nuovo_annuncio)
    await db.commit()

if __name__ == "__main__":
  data = load_data(sample_data_path)
  asyncio.run(insert_sample_data(data))
