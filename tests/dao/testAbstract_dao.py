import locale
import os
from datetime import datetime
from unittest import TestCase

from main.Models.Models import ProcedureModel, ArrestModel, CaseModel
from main.dao.arrest_dao import ArrestDao
from main.dao.dbtable import DbTable
from main.dao.local_properties_dao import LocalProperties

locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')


class TestAbstractDao(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.properties_path = "ressources/app-config-test.properties"
        cls.configs = LocalProperties(cls.properties_path)
        cls.root_path = os.path.abspath(os.path.dirname(__file__)) + "/../../"

        if not os.path.exists(cls.root_path + cls.configs.get("DB_DIRECTORY_PATH")):
            os.makedirs(cls.root_path + cls.configs.get("DB_DIRECTORY_PATH"))
        if os.path.exists(cls.root_path + cls.configs.get("DB_PATH")):
            os.remove(cls.root_path + cls.configs.get("DB_PATH"))


    def setUp(self):
        install = DbTable()
        install.db_connector.set_path(self.configs.get("DB_PATH"))
        install.create_arrests_table()

        self.arrestDao = ArrestDao()
        self.add_arrest_for_tests()

    def tearDown(self):
        os.remove(self.root_path + self.configs.get("DB_PATH"))

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
        self.numRole1 = "999111"
        cases1 = [CaseModel(numRole=self.numRole1)]
        self.arrest1 = ArrestModel(ref=self.ref1, arrest_date=decision_suspension_date1, language="fr",
                                   procedures=[procedure_suspension1, procedure_annulation1], pages=self.arrest1_pages,
                                   chamber="VI", cases=cases1)

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
        self.numRole2_1 = "999222"
        self.numRole2_2 = "888222"
        cases2 = [CaseModel(numRole=self.numRole2_1), CaseModel(numRole=self.numRole2_2)]
        self.arrest2 = ArrestModel(ref=self.ref2, arrest_date=decision_suspension_date2, language="fr",
                                   procedures=[procedure_suspension2, procedure_annulation2], cases=cases2)
        self.ref3 = 3
        self.arrest3_pages = 7
        self.arrest3 = ArrestModel(ref=self.ref3, arrest_date=decision_annulation_date2, language="fr",
                                   procedures=[procedure_suspension2, procedure_annulation2bis], chamber="VI",
                                   pages=self.arrest3_pages)

        request_suspension_date3 = datetime.strptime("15/07/2024", '%d/%m/%Y')
        decision_suspension_date3 = datetime.strptime("11/11/2024", '%d/%m/%Y')
        procedure3 = ProcedureModel(process=self.suspension, request_date=request_suspension_date3,
                                    decision_date=decision_suspension_date3, urgence=True)
        self.ref4 = 4
        self.arrest4 = ArrestModel(ref=self.ref4, arrest_date=decision_suspension_date3, language="fr",
                                   procedures=[procedure3])

        self.ref5 = 5
        self.arrest5 = ArrestModel(ref=self.ref5, language="fr")

        self.arrestDao.add(self.arrest1)
        self.arrestDao.add_all([self.arrest2, self.arrest3, self.arrest5])
        self.arrestDao.add(self.arrest4)
