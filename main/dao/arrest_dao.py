import locale
from datetime import datetime
from typing import List

from main.Arrest import Arrest
from main.dao.db_connector import DbConnector
from main.dao.local_properties_dao import LocalProperties

locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')
LAST_YEAR = datetime.now().year - 1


class ArrestDao:
    ARRESTS_TABLE_NAME = "arrests"
    REF = "ref"
    PUBLISH_DATE = "publish_date"
    CONTRACT_TYPE = "contract_type"

    def __init__(self, properties_path=LocalProperties.DEFAULT_PATH):
        configs = LocalProperties(properties_path)
        self.db_connector = DbConnector(configs.get("DB_PATH"))

    def get_arrests_for_year(self, year: int = LAST_YEAR):
        self.db_connector.create_connection()
        select_arrest = ("SELECT * FROM " + self.ARRESTS_TABLE_NAME + " WHERE " +
                         self.PUBLISH_DATE + " BETWEEN date(:begin) AND date(:last)")
        print(select_arrest)
        results = self.db_connector.execute_read_query(select_arrest,
                                                       {"begin": str(year) + '-01-01', "last": str(year) + '-12-31'})
        print(results)
        self.db_connector.close_connection()
        return [self._as_arrest(result) for result in results]

    def get_arrests_for_refs(self, refs: List):
        self.db_connector.create_connection()
        select_arrests = "SELECT * FROM " + self.ARRESTS_TABLE_NAME + " WHERE ref IN ( {refs}) ORDER BY ".format(
            refs=', '.join('?' for _ in refs)) + self.REF + " ASC"
        results = self.db_connector.execute_read_query(select_arrests, refs)
        self.db_connector.close_connection()
        return [self._as_arrest(result) for result in results]

    def get_arrest(self, ref: int):
        self.db_connector.create_connection()
        select_arrest = "SELECT * FROM " + self.ARRESTS_TABLE_NAME + " WHERE ref=:" + self.REF
        arrest = self.db_connector.execute_read_query(select_arrest, {self.REF: ref})
        self.db_connector.close_connection()
        return self._as_arrest(arrest[0])

    def add_arrest(self, arrest: Arrest):
        self.db_connector.create_connection()
        create_arrest = ("INSERT INTO " + self.ARRESTS_TABLE_NAME + " VALUES(:"
                         + self.REF + ", :" + self.PUBLISH_DATE + ", :" + self.CONTRACT_TYPE + ")")
        self.db_connector.execute_query(create_arrest, self._as_dict(arrest))
        self.db_connector.close_connection()

    def add_arrests(self, arrests):
        self.db_connector.create_connection()
        create_arrest = ("INSERT INTO " + self.ARRESTS_TABLE_NAME + " VALUES(:"
                         + self.REF + ", :" + self.PUBLISH_DATE + ", :" + self.CONTRACT_TYPE + ")")
        self.db_connector.execute_many_query(create_arrest, [self._as_dict(arrest) for arrest in arrests])
        self.db_connector.close_connection()

    def _as_dict(self, arrest: Arrest):
        return {self.REF: arrest.ref,
                self.PUBLISH_DATE: arrest.publish_date,
                self.CONTRACT_TYPE: arrest.contract_type}

    @staticmethod
    def _as_arrest(result_arrest):
        return Arrest(result_arrest[0], None, datetime.strptime(result_arrest[1], '%Y-%m-%d %H:%M:%S'),
                      result_arrest[2])
