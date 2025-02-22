import os
from datetime import datetime
from typing import List
from unittest import TestCase

from main.Models.Models import ArrestModel, ProcedureModel
from main.dao.arrest_dao import ArrestDao
from main.dao.dbtable import DbTable
from main.dao.local_properties_dao import LocalProperties


class TestArrestDao(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.properties_path = "ressources/app-config-test.properties"
        configs = LocalProperties(cls.properties_path)
        root_path = os.path.abspath(os.path.dirname(__file__)) + "/../../"

        if not os.path.exists(root_path + configs.get("DB_DIRECTORY_PATH")):
            os.makedirs(root_path + configs.get("DB_DIRECTORY_PATH"))
        if os.path.exists(root_path + configs.get("DB_PATH")):
            os.remove(root_path + configs.get("DB_PATH"))

        install = DbTable()
        install.db_connector.set_path(configs.get("DB_PATH"))
        install.create_arrests_table()

    def setUp(self):
        self.arrestDao = ArrestDao()
        self.add_arrest_for_tests()

    def tearDown(self):
        self.delete_arrests([self.arrest1, self.arrest2, self.arrest3, self.arrest4, self.arrest5])

    def delete_arrests(self, arrests):
        self.arrestDao.delete_all(arrests)

    def test_get_arrest(self):
        arrest_result: ArrestModel = self.arrestDao.get(self.ref1)
        self.assertEqual(self.ref1, arrest_result.ref)
        self.assertEqual(self.suspension, arrest_result.procedures[0].process)
        self.assertEqual(self.ref1, arrest_result.procedures[0].arrest_ref)

    def test_exist_arrest(self):
        self.assertTrue(self.arrestDao.exist(self.ref1))
        self.assertFalse(self.arrestDao.exist(657789))

    def test_update_arrest(self):
        new_pages = 7
        arrest_result: ArrestModel = self.arrestDao.get(self.ref1)
        self.assertEqual(self.ref1, arrest_result.ref)
        self.assertEqual(self.arrest1_pages, arrest_result.pages)
        self.assertNotEqual(new_pages, arrest_result.pages)

        self.arrest1.pages = new_pages
        self.arrestDao.add_update(self.arrest1)
        arrest_result2: ArrestModel = self.arrestDao.get(self.ref1)
        self.assertEqual(new_pages, arrest_result2.pages)


    def test_get_arrests(self):
        arrest_results: List["ArrestModel"] = self.arrestDao.get_all([self.ref1, self.ref2])
        self.assertEqual(2, len(arrest_results))
        self.assertEqual(self.ref1, arrest_results[0].ref)
        self.assertEqual(self.ref2, arrest_results[1].ref)

    def test_get_arrests_last_year(self):
        arrest_results: List["ArrestModel"] = self.arrestDao.get_for_last_year(2024)
        self.assertEqual(2, len(arrest_results))
        self.assertEqual(self.ref2, arrest_results[0].ref)
        self.assertEqual(self.ref4, arrest_results[1].ref)

    def add_arrest_for_tests(self):
        self.suspension = "Suspension"
        annulation = "Annulation"

        request_suspension_date1 = datetime.strptime("23/06/2023", '%d/%m/%Y')
        decision_suspension_date1 = datetime.strptime("12/10/2023", '%d/%m/%Y')
        request_annulation_date1 = datetime.strptime("23/06/2023", '%d/%m/%Y')
        procedure_suspension1 = ProcedureModel(process=self.suspension, request_date=request_suspension_date1,
                                               decision_date=decision_suspension_date1, urgence=False)
        procedure_annulation1 = ProcedureModel(process=annulation, request_date=request_annulation_date1,
                                               urgence=False)
        self.ref1 = 1
        self.arrest1_pages = 5
        self.arrest1 = ArrestModel(ref=self.ref1, arrest_date=decision_suspension_date1, language="fr",
                                   procedures=[procedure_suspension1, procedure_annulation1], pages=self.arrest1_pages)

        request_suspension_date2 = datetime.strptime("15/06/2024", '%d/%m/%Y')
        request_annulation_date2 = datetime.strptime("20/07/2024", '%d/%m/%Y')
        decision_suspension_date2 = datetime.strptime("12/10/2024", '%d/%m/%Y')
        decision_annulation_date2 = datetime.strptime("05/05/2025", '%d/%m/%Y')
        procedure_suspension2 = ProcedureModel(process=self.suspension, request_date=request_suspension_date2,
                                               decision_date=decision_suspension_date2, urgence=False)
        procedure_annulation2 = ProcedureModel(process=self.suspension, request_date=request_annulation_date2,
                                               urgence=False)
        procedure_annulation2bis = ProcedureModel(process=self.suspension, request_date=request_annulation_date2,
                                                  decision_date=decision_annulation_date2, urgence=False)
        self.ref2 = 2
        self.arrest2 = ArrestModel(ref=self.ref2, arrest_date=decision_suspension_date2, language="fr",
                                   procedures=[procedure_suspension2, procedure_annulation2])
        ref3 = 3
        self.arrest3 = ArrestModel(ref=ref3, arrest_date=decision_annulation_date2, language="fr",
                                   procedures=[procedure_suspension2, procedure_annulation2bis])

        request_suspension_date3 = datetime.strptime("15/07/2024", '%d/%m/%Y')
        decision_suspension_date3 = datetime.strptime("11/11/2024", '%d/%m/%Y')
        procedure3 = ProcedureModel(process=self.suspension, request_date=request_suspension_date3,
                                    decision_date=decision_suspension_date3, urgence=True)
        self.ref4 = 4
        self.arrest4 = ArrestModel(ref=self.ref4, arrest_date=decision_suspension_date3, language="fr",
                                   procedures=[procedure3])

        self.ref5 = 5
        self.arrest5 = ArrestModel(ref=self.ref5, language="fr")

        self.arrestDao.add_update(self.arrest1)
        self.arrestDao.add_all([self.arrest2, self.arrest3, self.arrest4, self.arrest5])
