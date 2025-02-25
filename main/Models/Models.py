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

REF = 'Réf.'
N_PAGES = 'Pages'
ERRORS = 'Erreurs'
ROLE_NUMBER = 'N° de Rôle'
RECTIF = 'Rectifié'
ARREST_DATE = 'Date de l\'arrêt'
ASK_PROCEDURE = 'Demande de procédure'
RULING = 'Décision'
KEYWORDS = 'Keywords'
CONTRACT_TYPE = 'Type de contrat'


class ArrestModel(BaseModel):
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

    procedures: Mapped[List["ProcedureModel"]] = relationship(back_populates='arrest', cascade="all, delete, delete-orphan")
    rulings: Mapped[List["RulingModel"]] = relationship(back_populates='arrest', cascade="all, delete, delete-orphan")
    keywords: Mapped[List["KeywordModel"]] = relationship(back_populates='arrest', cascade="all, delete, delete-orphan")

    cases: Mapped[List["CaseModel"]] = relationship(secondary=case_arrest_association, back_populates='arrests', cascade="all, delete, delete-orphan")
    errors: Mapped[List["ErrorModel"]] = relationship(back_populates='arrest', cascade="all, delete, delete-orphan")

    def get_path_to_pdf(self):
        return f"{self.path}/{self.ref}.pdf"

    def set_path(self):
        directory = self.arrest_date.strftime("%Y/%m") if self.arrest_date else "date_not_found"
        self.path = DEFAULT_ARRESTS_DIRECTORY.format(langue=self.language, chamber=self.chamber, date=directory)

    def as_dict(self):
        dic = {REF: self.ref,
               ERRORS: '\n'.join([error.message for error in self.errors]),
               N_PAGES: self.pages,
               ROLE_NUMBER: '\n'.join([case.numRole for case in self.cases]),
               RECTIF: self.is_rectified.real,
               CONTRACT_TYPE: self.contract_type,
               ARREST_DATE: self.arrest_date,
               ASK_PROCEDURE: ', '.join([pross.process for pross in self.procedures]),
               RULING: ', '.join([rul.get_label() for rul in self.rulings])
               }
        key_label = {}
        for keyword in self.keywords:
            if keyword.title not in key_label:
                key_label[keyword.title] = []
            key_label[keyword.title].append(keyword.word)
        return dic | key_label

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
    process = mapped_column(String)
    request_date = mapped_column(Date)
    decision_date = mapped_column(Date)
    urgence = mapped_column(Boolean)

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
    surplus = mapped_column(Boolean)
    arrest_ref: Mapped[int] = mapped_column(ForeignKey("arrest.ref"))
    arrest: Mapped["ArrestModel"] = relationship(back_populates='rulings')

    def get_label(self) -> str:
        surplus = " (rejet avec surplus)" if self.surplus else ""
        return f"{self.ruling}" + surplus

    def __repr__(self):
        return (f"<RulingModel(id={self.id}, name='{self.ruling}', "
                f"surplus={self.surplus}, "
                f"arrest_ref={self.arrest_ref})>")


class KeywordModel(BaseModel):
    __tablename__ = 'keyword'
    id: Mapped[int] = mapped_column(primary_key=True)
    title = mapped_column(String)
    word = mapped_column(String)
    arrest_ref: Mapped[int] = mapped_column(ForeignKey("arrest.ref"))
    arrest: Mapped["ArrestModel"] = relationship(back_populates='keywords')

    def __repr__(self):
        return (f"<KeywordModel(id={self.id}, title='{self.title}', word='{self.word}', "
                f"arrest_ref={self.arrest_ref})>")


class ErrorModel(BaseModel):
    __tablename__ = 'error'
    id: Mapped[int] = mapped_column(primary_key=True)
    message = mapped_column(String)
    arrest_ref: Mapped[int] = mapped_column(ForeignKey("arrest.ref"))
    arrest: Mapped["ArrestModel"] = relationship(back_populates='errors')

    def __repr__(self):
        return f"<ErrorModel(id={self.id}, message={self.message})>"
