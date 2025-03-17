import locale
from datetime import datetime, date
from typing import List

from sqlalchemy import select, exists, delete, and_

from main.models.models import ArrestModel
from main.models.converterModel import ConverterModel
from main.models.modelsDao import ArrestModelDao, ProcedureModelDao, RulingModelDao, KeywordModelDao, CaseModelDao, \
    ErrorModelDao
from main.dao.db_connector import DbConnector

locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')
LAST_YEAR = datetime.now().year - 1


class ArrestDao:

    def __init__(self):
        self.db_connector = DbConnector()
        self.session = self.db_connector.Session()
        self.converter = ConverterModel()

    def get_all(self, refs: List) -> List[ArrestModel]:
        stmt = select(ArrestModelDao).where(ArrestModelDao.ref.in_(refs)).order_by(ArrestModelDao.arrest_date)
        results = self.db_connector.read(lambda sess: sess.scalars(stmt).all(), session=self.session)
        return [self.converter.arrest_dao_to_model(result) for result in results]

    def get(self, ref: int) -> ArrestModel:
        stmt = select(ArrestModelDao).where(ArrestModelDao.ref.is_(ref))
        result = self.db_connector.read(lambda sess: sess.scalars(stmt).one(), session=self.session)
        return self.converter.arrest_dao_to_model(result)

    def get_last(self) -> ArrestModel:
        result = self.db_connector.read(
            lambda sess: sess.query(ArrestModelDao).order_by(ArrestModelDao.ref.desc()).first(),
            session=self.session)
        return self.converter.arrest_dao_to_model(result)

    def exist(self, ref: int)-> bool:
        stmt = exists().where(ArrestModelDao.ref.is_(ref))
        result = self.db_connector.read(lambda sess: sess.query(stmt).scalar(), session=self.session)
        return result

    def add(self, arrest: ArrestModel):
        arrest_dao = ArrestModelDao(
            ref=arrest.ref,
            pages=arrest.pages,
            contract_type=arrest.contract_type,
            is_rectified=arrest.is_rectified,
            arrest_date=arrest.arrest_date,
            avis=arrest.avis,
            chamber=arrest.chamber,
            language=arrest.language,
            en_causes=arrest.en_causes,
            contres=arrest.contres,
            intervenants=arrest.intervenants,
            path=arrest.path
        )

        self.session.add(arrest_dao)

        # Ajouter les procedures
        for procedure in arrest.procedures:
            procedure_dao = ProcedureModelDao(
                id=procedure.id,
                process=procedure.process,
                request_date=procedure.request_date,
                decision_date=procedure.decision_date,
                urgence=procedure.urgence,
                arrest_ref=arrest.ref
            )
            self.session.add(procedure_dao)

        # Ajouter les rulings
        for ruling in arrest.rulings:
            ruling_dao = RulingModelDao(
                id=ruling.id,
                ruling=ruling.ruling,
                surplus=ruling.surplus,
                arrest_ref=arrest.ref
            )
            self.session.add(ruling_dao)

        # Ajouter les keywords
        for keyword in arrest.keywords:
            keyword_dao = KeywordModelDao(
                id=keyword.id,
                title=keyword.title,
                word=keyword.word,
                arrest_ref=arrest.ref
            )
            self.session.add(keyword_dao)

        # Ajouter les cases
        for case in arrest.cases:
            case_dao = self.session.query(CaseModelDao).filter(CaseModelDao.numRole == case.numRole).first()
            if case_dao is None:
                case_dao = CaseModelDao(
                    numRole=case.numRole
                )
                self.session.add(case_dao)
            arrest_dao.cases.append(case_dao)

        # Ajouter les errors
        for error in arrest.errors:
            error_dao = ErrorModelDao(
                id=error.id,
                message=error.message,
                arrest_ref=arrest.ref
            )
            self.session.add(error_dao)

        self.session.commit()

    def add_all(self, arrests: List[ArrestModel]):
        arrests_dao = [self.converter.arrest_model_to_dao(arrest) for arrest in arrests]
        self.db_connector.execute(lambda sess: sess.add_all(arrests_dao), [arrest.ref for arrest in arrests_dao],
                                  session=self.session)

    def delete_all(self, refs: List[int]):
        stmt = delete(ArrestModelDao).where(ArrestModelDao.ref.in_(refs))
        self.db_connector.execute(lambda sess: sess.execute(stmt), refs, session=self.session)

    def delete(self, arrest: ArrestModel):
        arrest_dao = self.converter.arrest_model_to_dao(arrest)
        self.db_connector.execute(lambda sess: sess.delete(arrest_dao), arrest_dao.ref, session=self.session)

    def update(self, arrest: ArrestModel) -> ArrestModel:
        arrest_dao = self.session.query(ArrestModelDao).filter(ArrestModelDao.ref == arrest.ref).first()
        if arrest_dao is None:
            raise ValueError(f"Aucun arrêt trouvé avec la référence {arrest.ref}")

        arrest_dao.pages = arrest.pages
        arrest_dao.contract_type = arrest.contract_type
        arrest_dao.is_rectified = arrest.is_rectified
        arrest_dao.arrest_date = arrest.arrest_date
        arrest_dao.avis = arrest.avis
        arrest_dao.chamber = arrest.chamber
        arrest_dao.language = arrest.language
        arrest_dao.en_causes = arrest.en_causes
        arrest_dao.contres = arrest.contres
        arrest_dao.intervenants = arrest.intervenants
        arrest_dao.path = arrest.path

        # Mettre à jour les procedures
        for procedure in arrest.procedures:
            procedure_dao = self.session.query(ProcedureModelDao).filter(ProcedureModelDao.id == procedure.id).first()
            if procedure_dao is None:
                procedure_dao = ProcedureModelDao(
                    id=procedure.id,
                    process=procedure.process,
                    request_date=procedure.request_date,
                    decision_date=procedure.decision_date,
                    urgence=procedure.urgence,
                    arrest_ref=arrest.ref
                )
                self.session.add(procedure_dao)
            else:
                procedure_dao.process = procedure.process
                procedure_dao.request_date = procedure.request_date
                procedure_dao.decision_date = procedure.decision_date
                procedure_dao.urgence = procedure.urgence

        # Mettre à jour les rulings
        for ruling in arrest.rulings:
            ruling_dao = self.session.query(RulingModelDao).filter(RulingModelDao.id == ruling.id).first()
            if ruling_dao is None:
                ruling_dao = RulingModelDao(
                    id=ruling.id,
                    ruling=ruling.ruling,
                    surplus=ruling.surplus,
                    arrest_ref=arrest.ref
                )
                self.session.add(ruling_dao)
            else:
                ruling_dao.ruling = ruling.ruling
                ruling_dao.surplus = ruling.surplus

        # Mettre à jour les keywords
        for keyword in arrest.keywords:
            keyword_dao = self.session.query(KeywordModelDao).filter(KeywordModelDao.id == keyword.id).first()
            if keyword_dao is None:
                keyword_dao = KeywordModelDao(
                    id=keyword.id,
                    title=keyword.title,
                    word=keyword.word,
                    arrest_ref=arrest.ref
                )
                self.session.add(keyword_dao)
            else:
                keyword_dao.title = keyword.title
                keyword_dao.word = keyword.word

        # Mettre à jour les cases
        for case in arrest.cases:
            case_dao = self.session.query(CaseModelDao).filter(CaseModelDao.numRole == case.numRole).first()
            if case_dao is None:
                case_dao = CaseModelDao(
                    numRole=case.numRole
                )
                self.session.add(case_dao)

        # Mettre à jour les errors
        for error in arrest.errors:
            error_dao = self.session.query(ErrorModelDao).filter(ErrorModelDao.id == error.id).first()
            if error_dao is None:
                error_dao = ErrorModelDao(
                    id=error.id,
                    message=error.message,
                    arrest_ref=arrest.ref
                )
                self.session.add(error_dao)
            else:
                error_dao.message = error.message

        self.session.commit()
        return self.converter.arrest_dao_to_model(arrest_dao)

    def search_refs_and(self, **kwargs):
        query = select(ArrestModelDao.ref)
        conditions = []
        for attr, value in kwargs.items():
            if hasattr(ArrestModelDao, attr):
                if isinstance(value, list):
                    conditions.append(getattr(ArrestModelDao, attr).in_(value))
                else:
                    conditions.append(getattr(ArrestModelDao, attr).is_(value))
            else:
                raise ValueError(f"Invalid parameter value: {attr}={value}")
        if conditions:
            query = query.filter(and_(*conditions))
        return self.db_connector.read(lambda sess: sess.execute(query).scalars().all(), session=self.session)

    def search_arrests_for_year(self, year: int = LAST_YEAR):
        stmt = select(ArrestModelDao).where(
            ArrestModelDao.arrest_date.between(date(year, 1, 1), date(year + 1, 1, 1))).order_by(
            ArrestModelDao.arrest_date)
        results = self.db_connector.read(lambda sess: sess.scalars(stmt).all(), session=self.session)
        return [self.converter.arrest_dao_to_model(result) for result in results]
