from datetime import date
from typing import List

DEFAULT_ARRESTS_DIRECTORY = "result/arrests/{date}/{langue}/ch_{chamber}"

REF = 'Réf.'
LANGUE = 'Langue'
CHAMBER = 'Chambre'
N_PAGES = 'Pages'
ERRORS = 'Erreurs'
ROLE_NUMBER = 'N° de Rôle'
RECTIF = 'Rectifié'
ARREST_DATE = 'Date de l\'arrêt'
PROCEDURE = 'Procédure'
RULING = 'Décision'
KEYWORDS = 'Keywords'
CONTRACT_TYPE = 'Type de contrat'


class BaseModel:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class ArrestModel(BaseModel):
    def __init__(self, ref: int, pages: int = None, contract_type: str = None, is_rectified: bool = None,
                 arrest_date: date = None,
                 avis: str = None, chamber: str = None, language: str = None, en_causes: str = None,
                 contres: str = None, intervenants: str = None,
                 path: str = "result/arrests/no_path", procedures: List["ProcedureModel"] = None,
                 rulings: List["RulingModel"] = None,
                 keywords: List["KeywordModel"] = None, cases: List["CaseModel"] = None,
                 errors: List["ErrorModel"] = None):
        super().__init__()
        self.ref = ref
        self.pages = pages
        self.contract_type = contract_type
        self.is_rectified = is_rectified
        self.arrest_date = arrest_date
        self.avis = avis
        self.chamber = chamber
        self.language = language
        self.en_causes = en_causes
        self.contres = contres
        self.intervenants = intervenants
        self.path = path
        self.procedures = procedures if procedures else []
        self.rulings = rulings if rulings else []
        self.keywords = keywords if keywords else []
        self.cases = cases if cases else []
        self.errors = errors if errors else []

    def get_path_to_pdf(self):
        return f"{self.path}/{self.ref}.pdf"

    def set_path(self):
        directory = self.arrest_date.strftime("%Y/%m") if self.arrest_date else "date_not_found"
        self.path = DEFAULT_ARRESTS_DIRECTORY.format(langue=self.language, chamber=self.chamber, date=directory)

    def as_dict(self):
        dic = ({REF: self.ref,
                LANGUE: self.language,
                CHAMBER: self.chamber,
                N_PAGES: self.pages,
                ROLE_NUMBER: '\n'.join([case.numRole for case in self.cases]),
                RECTIF: self.is_rectified.real,
                CONTRACT_TYPE: self.contract_type,
                ARREST_DATE: self.arrest_date,
                PROCEDURE: ', '.join([pross.process for pross in self.procedures]),
                RULING: ', '.join([rul.get_label() for rul in self.rulings])
                } |
               self.get_key_labels())
        return dic | {ERRORS: '\n'.join([error.message for error in self.errors])}

    def get_key_labels(self):
        keywords = {}
        for keyword in self.keywords:
            if keyword.title not in keywords:
                keywords[keyword.title] = []
            keywords[keyword.title].append(keyword.word)
        key_labels = {}
        for title, words in keywords.items():
            key_labels[title] = ', '.join(words)
        return key_labels

    def __repr__(self):
        return (f"<ArrestModel(ref={self.ref}, pages={self.pages}, "
                f"contract_type={self.contract_type}, "
                f"is_rectified={self.is_rectified}, arrest_date={self.arrest_date}, "
                f"ask_procedures_count={len(self.procedures)}, "
                f"rulings_count={len(self.rulings)}, "
                f"keywords_count={len(self.keywords)})>")


class CaseModel(BaseModel):
    def __init__(self, num_role: str, arrests: List[ArrestModel] = None):
        super().__init__()
        self.numRole = num_role
        self.arrests = arrests if arrests else []

    def __repr__(self):
        return f"<CaseModel(numRole={self.numRole})>"


class ProcedureModel(BaseModel):
    def __init__(self, id: int = None, process: str = None, request_date: date = None, decision_date: date = None,
                 urgence: bool = None, arrest_ref: int = None, arrest: ArrestModel = None):
        super().__init__()
        self.id = id
        self.process = process
        self.request_date = request_date
        self.decision_date = decision_date
        self.urgence = urgence
        self.arrest_ref = arrest_ref
        self.arrest = arrest

    def __repr__(self):
        return (f"<ProcedureModel(id={self.id}, name='{self.process}', "
                f"request_date={self.request_date}, decision_date={self.decision_date}, "
                f"urgence={self.urgence}, arrest_ref={self.arrest_ref})>")


class RulingModel(BaseModel):
    def __init__(self, id: int = None, ruling: str = None, surplus: bool = None, arrest_ref: int = None,
                 arrest: ArrestModel = None):
        super().__init__()
        self.id = id
        self.ruling = ruling
        self.surplus = surplus
        self.arrest_ref = arrest_ref
        self.arrest = arrest

    def get_label(self) -> str:
        surplus = " avec surplus" if self.surplus else ""
        return f"{self.ruling}" + surplus

    def __repr__(self):
        return (f"<RulingModel(id={self.id}, name='{self.ruling}', "
                f"surplus={self.surplus}, "
                f"arrest_ref={self.arrest_ref})>")


class KeywordModel(BaseModel):
    def __init__(self, id: int = None, title: str = None, word: str = None, arrest_ref: int = None,
                 arrest: ArrestModel = None):
        super().__init__()
        self.id = id
        self.title = title
        self.word = word
        self.arrest_ref = arrest_ref
        self.arrest = arrest

    def __repr__(self):
        return (f"<KeywordModel(id={self.id}, title='{self.title}', word='{self.word}', "
                f"arrest_ref={self.arrest_ref})>")


class ErrorModel(BaseModel):
    def __init__(self, id: int = None, message: str = None, arrest_ref: int = None, arrest: ArrestModel = None):
        super().__init__()
        self.id = id
        self.message = message
        self.arrest_ref = arrest_ref
        self.arrest = arrest

    def __repr__(self):
        return f"<ErrorModel(id={self.id}, message={self.message})>"
