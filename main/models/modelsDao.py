from typing import List

from sqlalchemy import Column, Integer, Table, ForeignKey, Date, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase


class BaseModelDao(DeclarativeBase):
    pass


case_arrest_association = Table(
    'case_arrest', BaseModelDao.metadata,
    Column('case_id', Integer, ForeignKey('case.numRole')),
    Column('arrest_id', Integer, ForeignKey('arrest.ref'))
)


class ArrestModelDao(BaseModelDao):
    __tablename__ = 'arrest'
    ref: Mapped[int] = mapped_column(primary_key=True)
    pages = Column(Integer)
    contract_type = Column(String)
    is_rectified = mapped_column(Boolean)
    arrest_date = mapped_column(Date)
    avis = Column(String)  # Conforme / Contraire / Non qualifié / Pas d'avis
    chamber = Column(String)
    language = Column(String)  # fr / nl / de

    en_causes = Column(String)
    contres = Column(String)
    intervenants = Column(String)
    path = Column(String)

    procedures: Mapped[List["ProcedureModelDao"]] = relationship(back_populates='arrest',
                                                                 cascade="all, delete, delete-orphan")
    rulings: Mapped[List["RulingModelDao"]] = relationship(back_populates='arrest', cascade="all, delete, delete-orphan")
    keywords: Mapped[List["KeywordModelDao"]] = relationship(back_populates='arrest', cascade="all, delete, delete-orphan")

    cases: Mapped[List["CaseModelDao"]] = relationship(secondary=case_arrest_association, back_populates='arrests',
                                                       cascade="all, delete")
    errors: Mapped[List["ErrorModelDao"]] = relationship(back_populates='arrest', cascade="all, delete, delete-orphan")

    def __repr__(self):
        return (f"<ArrestModelDao(ref={self.ref}, pages={self.pages}, "
                f"contract_type={self.contract_type}, "
                f"is_rectified={self.is_rectified}, arrest_date={self.arrest_date}, "
                f"ask_procedures_count={len(self.procedures)}, "
                f"rulings_count={len(self.rulings)}, "
                f"keywords_count={len(self.keywords)})>")


class CaseModelDao(BaseModelDao):
    __tablename__ = 'case'
    numRole = mapped_column(String, primary_key=True)

    arrests: Mapped[List["ArrestModelDao"]] = relationship(secondary=case_arrest_association, back_populates='cases')

    def __repr__(self):
        return f"<CaseModelDao(numRole={self.numRole})>"


class ProcedureModelDao(BaseModelDao):
    __tablename__ = 'procedure'
    id: Mapped[int] = mapped_column(primary_key=True)
    process = mapped_column(String)
    request_date = mapped_column(Date)
    decision_date = mapped_column(Date)
    urgence = mapped_column(Boolean)

    arrest_ref: Mapped[int] = mapped_column(ForeignKey("arrest.ref"))
    arrest: Mapped["ArrestModelDao"] = relationship(back_populates='procedures')

    def __repr__(self):
        return (f"<ProcedureModelDao(id={self.id}, name='{self.process}', "
                f"request_date={self.request_date}, decision_date={self.decision_date}, "
                f"urgence={self.urgence}, arrest_ref={self.arrest_ref})>")


class RulingModelDao(BaseModelDao):
    __tablename__ = 'ruling'
    id: Mapped[int] = mapped_column(primary_key=True)
    ruling = Column(String)
    surplus = mapped_column(Boolean)
    arrest_ref: Mapped[int] = mapped_column(ForeignKey("arrest.ref"))
    arrest: Mapped["ArrestModelDao"] = relationship(back_populates='rulings')

    def __repr__(self):
        return (f"<RulingModelDao(id={self.id}, name='{self.ruling}', "
                f"surplus={self.surplus}, "
                f"arrest_ref={self.arrest_ref})>")


class KeywordModelDao(BaseModelDao):
    __tablename__ = 'keyword'
    id: Mapped[int] = mapped_column(primary_key=True)
    title = mapped_column(String)
    word = mapped_column(String)
    arrest_ref: Mapped[int] = mapped_column(ForeignKey("arrest.ref"))
    arrest: Mapped["ArrestModelDao"] = relationship(back_populates='keywords')

    def __repr__(self):
        return (f"<KeywordModelDao(id={self.id}, title='{self.title}', word='{self.word}', "
                f"arrest_ref={self.arrest_ref})>")


class ErrorModelDao(BaseModelDao):
    __tablename__ = 'error'
    id: Mapped[int] = mapped_column(primary_key=True)
    message = mapped_column(String)
    arrest_ref: Mapped[int] = mapped_column(ForeignKey("arrest.ref"))
    arrest: Mapped["ArrestModelDao"] = relationship(back_populates='errors')

    def __repr__(self):
        return f"<ErrorModelDao(id={self.id}, message={self.message})>"
