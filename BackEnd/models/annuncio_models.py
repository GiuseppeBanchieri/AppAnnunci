from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from database import Base


class Annuncio(Base):
  __tablename__ = 'annuncio'

  id: Mapped[int] = mapped_column(primary_key=True)
  codice_lingua_id = mapped_column(ForeignKey('codice_lingua.id', ondelete='SET NULL'), nullable=True)
  codice_lingua: Mapped[CodiceLingua | None] = relationship()
  titolo: Mapped[str] = mapped_column(String(100), nullable=False)
  contenuto: Mapped[str | None]
  pubblicato: Mapped[bool | None]
  categoria_id = mapped_column(ForeignKey('categoria.id', ondelete='SET NULL'), nullable=True)
  categoria: Mapped[Categoria | None] = relationship()
  sub_categoria_id = mapped_column(ForeignKey('sub_categoria.id', ondelete='SET NULL'), nullable=True)
  sub_categoria: Mapped[SubCategoria | None] = relationship()
  tipo_contratto_id = mapped_column(ForeignKey('tipo_contratto.id', ondelete='SET NULL'), nullable=True)
  tipo_contratto: Mapped[TipoContratto | None] = relationship()
  monte_ore_id = mapped_column(ForeignKey('monte_ore.id', ondelete='SET NULL'), nullable=True)
  monte_ore: Mapped[MonteOre | None] = relationship()
  smart_working: Mapped[bool | None]
  job_title: Mapped[str] = mapped_column(String(100))
  salario_min: Mapped[int | None]
  salario_max: Mapped[int | None]
  codice_valuta_id = mapped_column(ForeignKey('codice_valuta.id', ondelete='SET NULL'), nullable=True)
  codice_valuta: Mapped[CodiceValuta | None] = relationship()
  unita_erogazione_salario_id = mapped_column(ForeignKey('unita_erogazione_salario.id', ondelete='SET NULL'), nullable=True)
  unita_erogazione_salario: Mapped[UnitaErogazioneSalario | None] = relationship()
  datetime_pubblicazione: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
  datetime_chiusura: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default= None)
  regione_id = mapped_column(ForeignKey('regione.id', ondelete='SET NULL'), nullable=True)
  regione: Mapped[Regione | None] = relationship()
  citta_id = mapped_column(ForeignKey('citta.id', ondelete='SET NULL'), nullable=True)
  citta: Mapped[Citta | None] = relationship()
  formazione_id = mapped_column(ForeignKey('formazione.id', ondelete='SET NULL'), nullable=True)
  formazione: Mapped[Formazione | None] = relationship()


class CodiceLingua(Base):
  __tablename__ = 'codice_lingua'

  id: Mapped[int] = mapped_column(primary_key=True)
  codice: Mapped[str] = mapped_column(String(4), nullable=False, unique=True)

class Categoria(Base):
  __tablename__ = 'categoria'

  id: Mapped[int] = mapped_column(primary_key=True)
  categoria: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

class SubCategoria(Base):
  __tablename__ = 'sub_categoria'

  id: Mapped[int] = mapped_column(primary_key=True)
  sub_categoria: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
  categorie_id = mapped_column(ForeignKey('categoria.id', ondelete='CASCADE'))

class TipoContratto(Base):
  __tablename__ = 'tipo_contratto'

  id: Mapped[int] = mapped_column(primary_key=True)
  tipo: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

class MonteOre(Base):
  __tablename__ = 'monte_ore'

  id: Mapped[int] = mapped_column(primary_key=True)
  monte_ore: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

class CodiceValuta(Base):
  __tablename__ = 'codice_valuta'

  id: Mapped[int] = mapped_column(primary_key=True)
  codice: Mapped[str] = mapped_column(String(4), nullable=False, unique=True)

class UnitaErogazioneSalario(Base):
  __tablename__ = 'unita_erogazione_salario'

  id: Mapped[int] = mapped_column(primary_key=True)
  unita: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

class Regione(Base):
  __tablename__ = 'regione'

  id: Mapped[int] = mapped_column(primary_key=True)
  regione: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

class Citta(Base):
  __tablename__ = 'citta'

  id: Mapped[int] = mapped_column(primary_key=True)
  citta: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
  regione_id = mapped_column(ForeignKey('regione.id', ondelete='SET NULL'))

class Formazione(Base):
  __tablename__ = 'formazione'

  id: Mapped[int] = mapped_column(primary_key=True)
  titolo: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)