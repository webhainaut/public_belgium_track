import os
from datetime import datetime
from unittest import TestCase

from main.Arrest import Arrest
from main.dao.arrest_dao import ArrestDao
from main.dao.local_properties_dao import LocalProperties
from main.ressources.db_table import DbTable


class TestArrestDao(TestCase):

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

    def test_get_arrest(self):
        ref = 123456
        arrest = Arrest(ref, None, datetime.strptime("23/06/2023", '%d/%m/%Y'), "ceci")
        self.arrestDao.add_arrest(arrest)
        arrest_result = self.arrestDao.get_arrest(ref)
        self.assertEqual(arrest.ref, arrest_result.ref)
        self.assertEqual(arrest.publish_date, arrest_result.publish_date)
        self.assertEqual(arrest.contract_type, arrest_result.contract_type)

    def test_get_arrests_for_refs(self):
        ref1 = 123456
        arrest1 = Arrest(ref1, None, datetime.strptime("23/06/2023", '%d/%m/%Y'), "ceci")
        ref2 = 923456
        arrest2 = Arrest(ref2, None, datetime.strptime("27/06/2023", '%d/%m/%Y'), "cela")
        self.arrestDao.add_arrest(arrest1)
        self.arrestDao.add_arrest(arrest2)
        arrest_results = self.arrestDao.get_arrests_for_refs([ref1, ref2])
        self.assertEqual(len(arrest_results), 2)
        self.assertEqual(arrest1.ref, arrest_results[0].ref)
        self.assertEqual(arrest1.publish_date, arrest_results[0].publish_date)
        self.assertEqual(arrest1.contract_type, arrest_results[0].contract_type)
        self.assertEqual(arrest2.ref, arrest_results[1].ref)

    def test_add_arrests(self):
        ref1 = 123456
        arrest1 = Arrest(ref1, None, datetime.strptime("23/06/2023", '%d/%m/%Y'), "ceci")
        ref2 = 923456
        arrest2 = Arrest(ref2, None, datetime.strptime("27/06/2023", '%d/%m/%Y'), "cela")
        self.arrestDao.add_arrests([arrest1, arrest2])
        arrest_results = self.arrestDao.get_arrests_for_refs([ref1, ref2])
        self.assertEqual(len(arrest_results), 2)
        self.assertEqual(arrest1.ref, arrest_results[0].ref)
        self.assertEqual(arrest2.ref, arrest_results[1].ref)

    def test_get_arrests_for_year(self):
        ref1 = 123456
        arrest1 = Arrest(ref1, None, datetime.strptime("23/06/2023", '%d/%m/%Y'), "ceci")
        ref2 = 923456
        arrest2 = Arrest(ref2, None, datetime.strptime("27/06/2023", '%d/%m/%Y'), "cela")
        ref3 = 654789
        arrest3 = Arrest(ref3, None, datetime.strptime("02/05/2022", '%d/%m/%Y'), "cela")
        self.arrestDao.add_arrests([arrest1, arrest2, arrest3])
        arrest3_result = self.arrestDao.get_arrest(ref3)
        self.assertEqual(ref3, arrest3_result.ref)
        arrest_results = self.arrestDao.get_arrests_for_year(2023)
        self.assertEqual(len(arrest_results), 2)
        self.assertEqual(ref1, arrest_results[0].ref)
        self.assertEqual(ref2, arrest_results[1].ref)
