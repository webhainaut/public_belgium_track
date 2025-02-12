import os
from datetime import datetime
from typing import List
from unittest import TestCase

from main.Models.Models import ArrestModel, ProcedureModel
from main.dao.arrest_dao import ArrestDao
from main.dao.local_properties_dao import LocalProperties
from main.ressources.db_table import DbTable


class TestArrestDao(TestCase):

    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)

    def setUp(self):
        properties_path = "ressources/app-config-test.properties"
        configs = LocalProperties(properties_path)
        root_path = os.path.abspath(os.path.dirname(__file__)) + "/../../"

        if not os.path.exists(root_path + configs.get("DB_DIRECTORY_PATH")):
            os.makedirs(root_path + configs.get("DB_DIRECTORY_PATH"))
        if os.path.exists(root_path + configs.get("DB_PATH")):
            os.remove(root_path + configs.get("DB_PATH"))

        db_table = DbTable(configs)
        db_table.create_arrests_table()
        self.arrestDao = ArrestDao(properties_path)
        self.add_arrest_for_tests()

    def test_rapide(self):
        print("a")

    def add_arrest_for_tests(self):
        self.suspension = "Suspension"
        annulation = "Annulation"

        request_suspension_date1 = datetime.strptime("23/06/2023", '%d/%m/%Y')
        decision_suspension_date1 = datetime.strptime("12/10/2023", '%d/%m/%Y')
        request_annulation_date1 = datetime.strptime("23/06/2023", '%d/%m/%Y')
        procedure_suspension1 = ProcedureModel(name=self.suspension, request_date=request_suspension_date1,
                                               decision_date=decision_suspension_date1, urgence=False)
        procedure_annulation1 = ProcedureModel(name=annulation, request_date=request_annulation_date1,
                                               urgence=False)
        self.ref1 = 1
        arrest1 = ArrestModel(ref=self.ref1, arrest_date=decision_suspension_date1, language="fr",
                              procedures=[procedure_suspension1, procedure_annulation1])

        request_suspension_date2 = datetime.strptime("15/06/2024", '%d/%m/%Y')
        request_annulation_date2 = datetime.strptime("20/07/2024", '%d/%m/%Y')
        decision_suspension_date2 = datetime.strptime("12/10/2024", '%d/%m/%Y')
        decision_annulation_date2 = datetime.strptime("05/05/2025", '%d/%m/%Y')
        procedure_suspension2 = ProcedureModel(name=self.suspension, request_date=request_suspension_date2,
                                               decision_date=decision_suspension_date2, urgence=False)
        procedure_annulation2 = ProcedureModel(name=self.suspension, request_date=request_annulation_date2,
                                               urgence=False)
        procedure_annulation2bis = ProcedureModel(name=self.suspension, request_date=request_annulation_date2,
                                                  decision_date=decision_annulation_date2, urgence=False)
        self.ref2 = 2
        arrest2 = ArrestModel(ref=self.ref2, arrest_date=decision_suspension_date2, language="fr",
                              procedures=[procedure_suspension2, procedure_annulation2])
        ref3 = 3
        arrest3 = ArrestModel(ref=ref3, arrest_date=decision_annulation_date2, language="fr",
                              procedures=[procedure_suspension2, procedure_annulation2bis])

        request_suspension_date3 = datetime.strptime("15/07/2024", '%d/%m/%Y')
        decision_suspension_date3 = datetime.strptime("11/11/2024", '%d/%m/%Y')
        procedure3 = ProcedureModel(name=self.suspension, request_date=request_suspension_date3,
                                    decision_date=decision_suspension_date3, urgence=True)
        self.ref4 = 4
        arrest4 = ArrestModel(ref=self.ref4, arrest_date=decision_suspension_date3, language="fr",
                              procedures=[procedure3])

        self.ref5 = 5
        arrest5 = ArrestModel(ref=self.ref5, language="fr")

        self.arrestDao.add_arrests([arrest1, arrest2, arrest3, arrest4, arrest5])

    def test_get_arrest(self):
        arrest_result: ArrestModel = self.arrestDao.get_arrest(self.ref1)
        print(arrest_result)
        print(arrest_result.procedures[0])
        self.assertEqual(self.ref1, arrest_result.ref)
        self.assertEqual(self.suspension, arrest_result.procedures[0].name)
        self.assertEqual(self.ref1, arrest_result.procedures[0].arrest_ref)

    def test_get_arrests(self):
        arrest_results: List["ArrestModel"] = self.arrestDao.get_arrests([self.ref1, self.ref2])
        print(arrest_results)
        self.assertEqual(2, len(arrest_results))
        self.assertEqual(self.ref1, arrest_results[0].ref)
        self.assertEqual(self.ref2, arrest_results[1].ref)

    def test_get_arrests_last_year(self):
        arrest_results: List["ArrestModel"] = self.arrestDao.get_arrests_for_last_year(2024)
        print(arrest_results)
        self.assertEqual(2, len(arrest_results))
        self.assertEqual(self.ref2, arrest_results[0].ref)
        self.assertEqual(self.ref4, arrest_results[1].ref)
