from typing import List

from sqlalchemy import Column, Integer, Table, ForeignKey, Date, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase


class BaseModel(DeclarativeBase):
    pass


case_arrest_association = Table(
    'case_arrest', BaseModel.metadata,
    Column('case_id', Integer, ForeignKey('case.numRole')),
    Column('arrest_id', Integer, ForeignKey('arrest.ref'))
)

DEFAULT_ARRESTS_DIRECTORY = "result/arrests/{langue}/ch_{chamber}/{date}"


class ArrestModel(BaseModel):
    __tablename__ = 'arrest'
    ref: Mapped[int] = mapped_column(primary_key=True)
    pages = Column(Integer)
    contract_type = Column(String)
    is_rectified = Column(Boolean)
    arrest_date = mapped_column(Date)
    avis = Column(String)  # Conforme / Contraire / Non qualifié / Pas d'avis
    chamber = Column(Integer)  # > 0
    language = Column(String)  # fr / nl / de

    en_causes = Column(String)
    contres = Column(String)
    intervenants = Column(String)
    path = Column(String)

    procedures: Mapped[List["ProcedureModel"]] = relationship(back_populates='arrest', cascade="all, delete")
    rulings: Mapped[List["RulingModel"]] = relationship(back_populates='arrest', cascade="all, delete")
    keywords: Mapped[List["KeywordModel"]] = relationship(back_populates='arrest', cascade="all, delete")

    cases: Mapped[List["CaseModel"]] = relationship(secondary=case_arrest_association, back_populates='arrests')
    errors: Mapped[List["ErrorModel"]] = relationship(back_populates='arrest', cascade="all, delete")

    def get_path_to_pdf(self):
        return f"{self.path}/{self.ref}.pdf"

    def set_path(self):
        if self.arrest_date is None:
            directory = "date_not_found"
        else:
            directory = self.arrest_date.strftime("%Y/%m")
        self.path = DEFAULT_ARRESTS_DIRECTORY.format(langue=self.language, chamber=self.chamber, date=directory)

    def __repr__(self):
        return (f"<ArrestModel(ref={self.ref}, pages={self.pages}, "
                f"contract_type={self.contract_type}, "
                f"is_rectified={self.is_rectified}, arrest_date={self.arrest_date}, "
                f"ask_procedures_count={len(self.procedures)}, "
                f"rulings_count={len(self.rulings)}, "
                f"keywords_count={len(self.keywords)})>")


class CaseModel(BaseModel):
    __tablename__ = 'case'
    numRole = mapped_column(String, primary_key=True)

    arrests: Mapped[List["ArrestModel"]] = relationship(secondary=case_arrest_association, back_populates='cases')

    def __repr__(self):
        return f"<CaseModel(numRole={self.numRole})>"


class ProcedureModel(BaseModel):
    __tablename__ = 'procedure'
    id: Mapped[int] = mapped_column(primary_key=True)
    process = Column(String)
    request_date = Column(Date)
    decision_date = Column(Date)
    urgence = Column(Boolean)

    arrest_ref: Mapped[int] = mapped_column(ForeignKey("arrest.ref"))
    arrest: Mapped["ArrestModel"] = relationship(back_populates='procedures')

    def __repr__(self):
        return (f"<ProcedureModel(id={self.id}, name='{self.process}', "
                f"request_date={self.request_date}, decision_date={self.decision_date}, "
                f"urgence={self.urgence}, arrest_ref={self.arrest_ref})>")


class RulingModel(BaseModel):
    __tablename__ = 'ruling'
    id: Mapped[int] = mapped_column(primary_key=True)
    ruling = Column(String)
    surplus = Column(Boolean)
    arrest_ref: Mapped[int] = mapped_column(ForeignKey("arrest.ref"))
    arrest: Mapped["ArrestModel"] = relationship(back_populates='rulings')

    def __repr__(self):
        return (f"<RulingModel(id={self.id}, name='{self.ruling}', "
                f"surplus={self.surplus}, "
                f"arrest_ref={self.arrest_ref})>")


class KeywordModel(BaseModel):
    __tablename__ = 'keyword'
    id: Mapped[int] = mapped_column(primary_key=True)
    title = Column(String)
    word = Column(String)
    arrest_ref: Mapped[int] = mapped_column(ForeignKey("arrest.ref"))
    arrest: Mapped["ArrestModel"] = relationship(back_populates='keywords')

    def __repr__(self):
        return (f"<KeywordModel(id={self.id}, title='{self.title}', word='{self.word}', "
                f"arrest_ref={self.arrest_ref})>")


class ErrorModel(BaseModel):
    __tablename__ = 'error'
    id: Mapped[int] = mapped_column(primary_key=True)
    message = Column(String)
    arrest_ref: Mapped[int] = mapped_column(ForeignKey("arrest.ref"))
    arrest: Mapped["ArrestModel"] = relationship(back_populates='errors')

    def __repr__(self):
        return f"<ErrorModel(id={self.id}, message={self.message})>"
