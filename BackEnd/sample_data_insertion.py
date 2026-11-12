import json
from sqlalchemy import select
from datetime import datetime
from typing import List, Dict
import re

from database import SessionLocal
from models import annuncio_models as models
from schemas.sample_data_schema import AnnuncioSampleData

#Classe da usare una volta sola per inserire i dati campione degli annunci e delle tabelle di metadati
class SampleDataInsertionService:

  def __init__(self):
    self.db = SessionLocal()

  def load_data(self) -> List[Dict]:
    with open('./test_data/job_postings_2000.json', 'r', encoding='utf-8') as file:
      data: List[Dict] = json.load(file)
      return data

  def sanitize_string_input(self, string_input: str) -> str:
    #funzione per sanitizzare l'input str di metadati che devono essere unique. Questa sanitizzazione serve solo ad avere un formatting consistente per questi valori.
    return re.sub(r'\s+', ' ', string_input.strip().lower())

  def insert_sample_annuncio(self, annuncio: AnnuncioSampleData) -> None:

    query_annuncio_db = self.db.scalars(select(models.Annuncio.id).where(models.Annuncio.id == annuncio.id)).first()
    if query_annuncio_db is None:
      nuovo_annuncio_db = models.Annuncio(**annuncio.model_dump())
      self.db.add(nuovo_annuncio_db)
      self.db.commit()

  
  def insert_sample_data(self, data: list) -> None:
    for row in data:
      nuovo_annuncio_id: int = row['id']

      nuovo_codice_lingua = self.sanitize_string_input(row['languageCode'])
      codice_lingua_id: int | None = self.db.scalars(select(models.CodiceLingua.id).where(models.CodiceLingua.codice == nuovo_codice_lingua)).first()
      if codice_lingua_id is None:
        print('Inserimento nuovo codice lingua')
        nuovo_codice_lingua_db = models.CodiceLingua(codice = nuovo_codice_lingua)
        self.db.add(nuovo_codice_lingua_db)
        self.db.commit()
        nuovo_codice_lingua = nuovo_codice_lingua_db.id
      else:
        nuovo_codice_lingua = codice_lingua_id

      nuovo_titolo: str = row['title']
      nuovo_contenuto: str = row['description']
      nuovo_pubblicato: bool = row['isPublished']

      nuova_categoria = self.sanitize_string_input(row['jobClassification']['category'])
      categoria_id: int | None = self.db.scalars(select(models.Categoria.id).where(models.Categoria.categoria == nuova_categoria)).first()
      if categoria_id is None:
        print('Inserimento nuova categoria')
        nuova_categoria_db = models.Categoria(categoria = nuova_categoria)
        self.db.add(nuova_categoria_db)
        self.db.commit()
        nuova_categoria = nuova_categoria_db.id
      else:
        nuova_categoria = categoria_id

      nuova_sub_categoria = self.sanitize_string_input(row['jobClassification']['subCategory'])
      sub_categoria_id: int | None = self.db.scalars(select(models.SubCategoria.id).where(models.SubCategoria.sub_categoria == nuova_sub_categoria)).first()
      if sub_categoria_id is None:
        print('Inserimento nuova sub categoria')
        nuova_sub_categoria_db = models.SubCategoria(sub_categoria = nuova_sub_categoria, categorie_id = nuova_categoria)
        self.db.add(nuova_sub_categoria_db)
        self.db.commit()
        nuova_sub_categoria = nuova_sub_categoria_db.id
      else:
        nuova_sub_categoria = sub_categoria_id

      nuovo_tipo_contratto = self.sanitize_string_input(row['jobInformation']['jobTypes'][0])
      tipo_contratto_id: int | None = self.db.scalars(select(models.TipoContratto.id).where(models.TipoContratto.tipo == nuovo_tipo_contratto)).first()
      if tipo_contratto_id is None:
        print('Inserimento nuovo tipo contratto')
        nuovo_tipo_contratto_db = models.TipoContratto(tipo = nuovo_tipo_contratto)
        self.db.add(nuovo_tipo_contratto_db)
        self.db.commit()
        nuovo_tipo_contratto = nuovo_tipo_contratto_db.id
      else:
        nuovo_tipo_contratto = tipo_contratto_id

      nuovo_monte_ore = self.sanitize_string_input(row['jobInformation']['expectedHoursOfService'])
      monte_ore_id: int | None = self.db.scalars(select(models.MonteOre.id).where(models.MonteOre.monte_ore == nuovo_monte_ore)).first()
      if monte_ore_id is None:
        print('Inserimento nuovo monte ore')
        nuovo_monte_ore_db = models.MonteOre(monte_ore = nuovo_monte_ore)
        self.db.add(nuovo_monte_ore_db)
        self.db.commit()
        nuovo_monte_ore = nuovo_monte_ore_db.id
      else:
        nuovo_monte_ore = monte_ore_id

      nuovo_smart_working: bool = row['jobInformation']['remoteWorkAllowed']
      nuovo_job_title: str = self.sanitize_string_input(row['jobTitle'])
      nuovo_salario_min: int = row['payRates']['salaryMin']
      nuovo_salario_max: int = row['payRates']['salaryMax']

      nuovo_codice_valuta = self.sanitize_string_input(row['payRates']['currencyCode'])
      codice_valuta_id: int | None =  self.db.scalars(select(models.CodiceValuta.id).where(models.CodiceValuta.codice == nuovo_codice_valuta)).first()
      if codice_valuta_id is None:
        print('Inserimento nuovo codice valuta')
        nuovo_codice_valuta_db = models.CodiceValuta(codice = nuovo_codice_valuta)
        self.db.add(nuovo_codice_valuta_db)
        self.db.commit()
        nuovo_codice_valuta = nuovo_codice_valuta_db.id
      else:
        nuovo_codice_valuta = codice_valuta_id

      nuova_unita_erogazione_salario = self.sanitize_string_input(row['payRates']['unit'])
      unita_erogazione_salario_id: int | None = self.db.scalars(select(models.UnitaErogazioneSalario.id).where(models.UnitaErogazioneSalario.unita == nuova_unita_erogazione_salario)).first()
      if unita_erogazione_salario_id is None:
        print('Inserimento nuova unita erogazione salario')
        nuova_unita_erogazione_salario_db = models.UnitaErogazioneSalario(unita = nuova_unita_erogazione_salario)
        self.db.add(nuova_unita_erogazione_salario_db)
        self.db.commit()
        nuova_unita_erogazione_salario = nuova_unita_erogazione_salario_db.id
      else:
        nuova_unita_erogazione_salario = unita_erogazione_salario_id

      nuovo_datetime_pubblicazione: datetime = row['postingDetail']['postingTime']
      nuovo_datetime_chiusura : datetime | None = row['postingDetail']['closingTime']

      nuova_regione = self.sanitize_string_input(row['workLocationAddress']['administrativeArea'])
      regione_id: int | None = self.db.scalars(select(models.Regione.id).where(models.Regione.regione == nuova_regione)).first()
      if regione_id is None:
        print('Inserimento di una nuova regione')
        nuova_regione_db = models.Regione(regione = nuova_regione)
        self.db.add(nuova_regione_db)
        self.db.commit()
        nuova_regione = nuova_regione_db.id
      else:
        nuova_regione = regione_id

      nuova_citta = self.sanitize_string_input(row['workLocationAddress']['locality'])
      citta_id: int | None = self.db.scalars(select(models.Citta.id).where(models.Citta.citta == nuova_citta)).first()
      if citta_id is None:
        print('Inserimento nuova città')
        nuova_citta_db = models.Citta(citta = nuova_citta, regione_id = nuova_regione)
        self.db.add(nuova_citta_db)
        self.db.commit()
        nuova_citta = nuova_citta_db.id
      else:
        nuova_citta = citta_id

      nuova_formazione = self.sanitize_string_input(row['education']['degree'])
      formazione_id: int | None = self.db.scalars(select(models.Formazione.id).where(models.Formazione.titolo == nuova_formazione)).first()
      if formazione_id is None:
        print('Inserimento nuova formazione')
        nuova_formazione_db = models.Formazione(titolo = nuova_formazione)
        self.db.add(nuova_formazione_db)
        self.db.commit()
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
      
      self.insert_sample_annuncio(nuovo_annuncio)
      

      
      

service = SampleDataInsertionService()
data = service.load_data()
service.insert_sample_data(data)
