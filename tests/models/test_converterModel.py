import unittest
from datetime import date
from unittest import TestCase

from main.models.models import ArrestModel, KeywordModel, RulingModel, ProcedureModel
from main.models.modelsDao import ArrestModelDao, KeywordModelDao, RulingModelDao, ProcedureModelDao
from main.models.converterModel import ConverterModel


class TestConverterModel(TestCase):


    def setUp(self):
        self.converter = ConverterModel()

    def test_arrest_model_to_dao(self):
        # Create an instance of ArrestModel
        arrest_model = ArrestModel(
            ref=65587,
            pages=52,
            contract_type="contract_type",
            is_rectified=True,
            arrest_date=date(2022, 1, 1),
            avis="avis",
            chamber="chamber",
            language="language",
            en_causes="en_causes",
            contres="contres",
            intervenants="intervenants",
            path="path",
            procedures=[],
            rulings=[],
            keywords=[],
            cases=[],
            errors=[]
        )

        # Convert ArrestModel to ArrestModelDao
        arrest_dao = self.converter.arrest_model_to_dao(arrest_model)

        # Check if all attributes are correctly converted
        self.assertEqual(arrest_dao.ref, arrest_model.ref)
        self.assertEqual(arrest_dao.pages, arrest_model.pages)
        self.assertEqual(arrest_dao.contract_type, arrest_model.contract_type)
        self.assertEqual(arrest_dao.is_rectified, arrest_model.is_rectified)
        self.assertEqual(arrest_dao.arrest_date, arrest_model.arrest_date)
        self.assertEqual(arrest_dao.avis, arrest_model.avis)
        self.assertEqual(arrest_dao.chamber, arrest_model.chamber)
        self.assertEqual(arrest_dao.language, arrest_model.language)
        self.assertEqual(arrest_dao.en_causes, arrest_model.en_causes)
        self.assertEqual(arrest_dao.contres, arrest_model.contres)
        self.assertEqual(arrest_dao.intervenants, arrest_model.intervenants)
        self.assertEqual(arrest_dao.path, arrest_model.path)
        self.assertEqual(arrest_dao.procedures, [])
        self.assertEqual(arrest_dao.rulings, [])
        self.assertEqual(arrest_dao.keywords, [])
        self.assertEqual(arrest_dao.cases, [])
        self.assertEqual(arrest_dao.errors, [])

    def test_arrest_dao_to_model(self):
        # Create an instance of ArrestModelDao
        arrest_dao = ArrestModelDao(
            ref=99846,
            pages=5,
            contract_type="contract_type",
            is_rectified=True,
            arrest_date=date(2022, 1, 1),
            avis="avis",
            chamber="chamber",
            language="language",
            en_causes="en_causes",
            contres="contres",
            intervenants="intervenants",
            path="path",
            procedures=[],
            rulings=[],
            keywords=[],
            cases=[],
            errors=[]
        )

        # Convert ArrestModelDao to ArrestModel
        arrest_model = self.converter.arrest_dao_to_model(arrest_dao)

        # Check if all attributes are correctly converted
        self.assertEqual(arrest_model.ref, arrest_dao.ref)
        self.assertEqual(arrest_model.pages, arrest_dao.pages)
        self.assertEqual(arrest_model.contract_type, arrest_dao.contract_type)
        self.assertEqual(arrest_model.is_rectified, arrest_dao.is_rectified)
        self.assertEqual(arrest_model.arrest_date, arrest_dao.arrest_date)
        self.assertEqual(arrest_model.avis, arrest_dao.avis)
        self.assertEqual(arrest_model.chamber, arrest_dao.chamber)
        self.assertEqual(arrest_model.language, arrest_dao.language)
        self.assertEqual(arrest_model.en_causes, arrest_dao.en_causes)
        self.assertEqual(arrest_model.contres, arrest_dao.contres)
        self.assertEqual(arrest_model.intervenants, arrest_dao.intervenants)
        self.assertEqual(arrest_model.path, arrest_dao.path)
        self.assertEqual(arrest_model.procedures, [])
        self.assertEqual(arrest_model.rulings, [])
        self.assertEqual(arrest_model.keywords, [])
        self.assertEqual(arrest_model.cases, [])
        self.assertEqual(arrest_model.errors, [])

    def test_procedure_model_to_dao(self):
        # Create an instance of ProcedureModel
        procedure_model = ProcedureModel(
            id=1,
            process="process",
            request_date=date(2022, 1, 1),
            decision_date=date(2022, 1, 2),
            urgence=True,
            arrest_ref=8254
        )

        # Convert ProcedureModel to ProcedureModelDao
        procedure_dao = self.converter.procedure_model_to_dao(procedure_model)

        # Check if all attributes are correctly converted
        self.assertEqual(procedure_dao.id, procedure_model.id)
        self.assertEqual(procedure_dao.process, procedure_model.process)
        self.assertEqual(procedure_dao.request_date, procedure_model.request_date)
        self.assertEqual(procedure_dao.decision_date, procedure_model.decision_date)
        self.assertEqual(procedure_dao.urgence, procedure_model.urgence)
        self.assertEqual(procedure_dao.arrest_ref, procedure_model.arrest_ref)

    def test_procedure_dao_to_model(self):
        # Create an instance of ProcedureModelDao
        procedure_dao = ProcedureModelDao(
            id=1,
            process="process",
            request_date=date(2022, 1, 1),
            decision_date=date(2022, 1, 2),
            urgence=True,
            arrest_ref=98765
        )

        # Convert ProcedureModelDao to ProcedureModel
        procedure_model = self.converter.procedure_dao_to_model(procedure_dao)

        # Check if all attributes are correctly converted
        self.assertEqual(procedure_model.id, procedure_dao.id)
        self.assertEqual(procedure_model.process, procedure_dao.process)
        self.assertEqual(procedure_model.request_date, procedure_dao.request_date)
        self.assertEqual(procedure_model.decision_date, procedure_dao.decision_date)
        self.assertEqual(procedure_model.urgence, procedure_dao.urgence)
        self.assertEqual(procedure_model.arrest_ref, procedure_dao.arrest_ref)

    def test_ruling_model_to_dao(self):
        # Create an instance of RulingModel
        ruling_model = RulingModel(
            id=1,
            ruling="ruling",
            surplus=True,
            arrest_ref=56478
        )

        # Convert RulingModel to RulingModelDao
        ruling_dao = self.converter.ruling_model_to_dao(ruling_model)

        # Check if all attributes are correctly converted
        self.assertEqual(ruling_dao.id, ruling_model.id)
        self.assertEqual(ruling_dao.ruling, ruling_model.ruling)
        self.assertEqual(ruling_dao.surplus, ruling_model.surplus)
        self.assertEqual(ruling_dao.arrest_ref, ruling_model.arrest_ref)

    def test_ruling_dao_to_model(self):
        # Create an instance of RulingModelDao
        ruling_dao = RulingModelDao(
            id=1,
            ruling="ruling",
            surplus=True,
            arrest_ref=9874
        )

        # Convert RulingModelDao to RulingModel
        ruling_model = self.converter.ruling_dao_to_model(ruling_dao)

        # Check if all attributes are correctly converted
        self.assertEqual(ruling_model.id, ruling_dao.id)
        self.assertEqual(ruling_model.ruling, ruling_dao.ruling)
        self.assertEqual(ruling_model.surplus, ruling_dao.surplus)
        self.assertEqual(ruling_model.arrest_ref, ruling_dao.arrest_ref)

    def test_keyword_model_to_dao(self):
        # Create an instance of KeywordModel
        keyword_model = KeywordModel(
            id=1,
            title="title",
            word="word",
            arrest_ref=78445
        )

        # Convert KeywordModel to KeywordModelDao
        keyword_dao = self.converter.keyword_model_to_dao(keyword_model)

        # Check if all attributes are correctly converted
        self.assertEqual(keyword_dao.id, keyword_model.id)
        self.assertEqual(keyword_dao.title, keyword_model.title)
        self.assertEqual(keyword_dao.word, keyword_model.word)
        self.assertEqual(keyword_dao.arrest_ref, keyword_model.arrest_ref)

    def test_keyword_dao_to_model(self):
        # Create an instance of KeywordModelDao
        keyword_dao = KeywordModelDao(
            id=1,
            title="title",
            word="word",
            arrest_ref=856
        )

        # Convert KeywordModelDao to KeywordModel
        keyword_model = self.converter.keyword_dao_to_model(keyword_dao)

        # Check if all attributes are correctly converted
        self.assertEqual(keyword_model.id, keyword_dao.id)
        self.assertEqual(keyword_model.title, keyword_dao.title)
        self.assertEqual(keyword_model.word, keyword_dao.word)
        self.assertEqual(keyword_model.arrest_ref, keyword_dao.arrest_ref)

if __name__ == '__main__':
    unittest.main()
