from main.models.models import ArrestModel, ProcedureModel, RulingModel, ErrorModel, CaseModel, KeywordModel
from main.models.modelsDao import ArrestModelDao, ProcedureModelDao, RulingModelDao, ErrorModelDao, CaseModelDao, \
    KeywordModelDao


class ConverterModel:
    def arrest_model_to_dao(self, arrest_model: ArrestModel) -> ArrestModelDao:
        arrest_dao = ArrestModelDao(
            ref=arrest_model.ref,
            pages=arrest_model.pages,
            contract_type=arrest_model.contract_type,
            is_rectified=arrest_model.is_rectified,
            arrest_date=arrest_model.arrest_date,
            avis=arrest_model.avis,
            chamber=arrest_model.chamber,
            language=arrest_model.language,
            en_causes=arrest_model.en_causes,
            contres=arrest_model.contres,
            intervenants=arrest_model.intervenants,
            path=arrest_model.path
        )
        arrest_dao.procedures  = [self.procedure_model_to_dao(procedure) for procedure in arrest_model.procedures]
        arrest_dao.rulings = [self.ruling_model_to_dao(ruling) for ruling in arrest_model.rulings]
        arrest_dao.keywords = [self.keyword_model_to_dao(keyword) for keyword in arrest_model.keywords]
        arrest_dao.cases = [self.case_model_to_dao(case) for case in arrest_model.cases]
        arrest_dao.errors = [self.error_model_to_dao(error) for error in arrest_model.errors]

        return arrest_dao

    def arrest_dao_to_model(self, arrest_dao: ArrestModelDao) -> ArrestModel:
        arrest_model = ArrestModel(
            ref=arrest_dao.ref,
            pages=arrest_dao.pages,
            contract_type=arrest_dao.contract_type,
            is_rectified=arrest_dao.is_rectified,
            arrest_date=arrest_dao.arrest_date,
            avis=arrest_dao.avis,
            chamber=arrest_dao.chamber,
            language=arrest_dao.language,
            en_causes=arrest_dao.en_causes,
            contres=arrest_dao.contres,
            intervenants=arrest_dao.intervenants,
            path=arrest_dao.path,
            procedures=[self.procedure_dao_to_model(procedure) for procedure in arrest_dao.procedures],
            rulings=[self.ruling_dao_to_model(ruling) for ruling in arrest_dao.rulings],
            keywords=[self.keyword_dao_to_model(keyword) for keyword in arrest_dao.keywords],
            cases=[self.case_dao_to_model(case) for case in arrest_dao.cases],
            errors=[self.error_dao_to_model(error) for error in arrest_dao.errors]
        )
        return arrest_model

    @staticmethod
    def procedure_model_to_dao(procedure_model: ProcedureModel) -> ProcedureModelDao:
        procedure_dao = ProcedureModelDao(
            id=procedure_model.id,
            process=procedure_model.process,
            request_date=procedure_model.request_date,
            decision_date=procedure_model.decision_date,
            urgence=procedure_model.urgence,
            arrest_ref=procedure_model.arrest_ref
        )
        return procedure_dao

    @staticmethod
    def ruling_model_to_dao(ruling_model: RulingModel) -> RulingModelDao:
        ruling_dao = RulingModelDao(
            id=ruling_model.id,
            ruling=ruling_model.ruling,
            surplus=ruling_model.surplus,
            arrest_ref=ruling_model.arrest_ref
        )
        return ruling_dao

    @staticmethod
    def keyword_model_to_dao(keyword_model: KeywordModel) -> KeywordModelDao:
        keyword_dao = KeywordModelDao(
            id=keyword_model.id,
            title=keyword_model.title,
            word=keyword_model.word,
            arrest_ref=keyword_model.arrest_ref
        )
        return keyword_dao

    @staticmethod
    def case_model_to_dao(case_model: CaseModel) -> CaseModelDao:
        case_dao = CaseModelDao(
            numRole=case_model.numRole
        )
        return case_dao

    @staticmethod
    def error_model_to_dao(error_model: ErrorModel) -> ErrorModelDao:
        error_dao = ErrorModelDao(
            id=error_model.id,
            message=error_model.message,
            arrest_ref=error_model.arrest_ref
        )
        return error_dao

    @staticmethod
    def procedure_dao_to_model(procedure_dao: ProcedureModelDao) -> ProcedureModel:
        procedure_model = ProcedureModel(
            id=procedure_dao.id,
            process=procedure_dao.process,
            request_date=procedure_dao.request_date,
            decision_date=procedure_dao.decision_date,
            urgence=procedure_dao.urgence,
            arrest_ref=procedure_dao.arrest_ref
        )
        return procedure_model

    @staticmethod
    def ruling_dao_to_model(ruling_dao: RulingModelDao) -> RulingModel:
        ruling_model = RulingModel(
            id=ruling_dao.id,
            ruling=ruling_dao.ruling,
            surplus=ruling_dao.surplus,
            arrest_ref=ruling_dao.arrest_ref
        )
        return ruling_model

    @staticmethod
    def keyword_dao_to_model(keyword_dao: KeywordModelDao) -> KeywordModel:
        keyword_model = KeywordModel(
            id=keyword_dao.id,
            title=keyword_dao.title,
            word=keyword_dao.word,
            arrest_ref=keyword_dao.arrest_ref
        )
        return keyword_model

    @staticmethod
    def case_dao_to_model(case_dao: CaseModelDao) -> CaseModel:
        case_model = CaseModel(
            num_role=case_dao.numRole
        )
        return case_model

    @staticmethod
    def error_dao_to_model(error_dao: ErrorModelDao) -> ErrorModel:
        error_model = ErrorModel(
            id=error_dao.id,
            message=error_dao.message,
            arrest_ref=error_dao.arrest_ref
        )
        return error_model