import locale
from datetime import datetime, date
from typing import List

from sqlalchemy import select

from main.Arrest import Arrest
from main.Models.Models import ArrestModel
from main.dao.db_connector import DbConnector
from main.dao.local_properties_dao import LocalProperties

locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')
LAST_YEAR = datetime.now().year - 1


class ArrestDao:

    def __init__(self, properties_path=LocalProperties.DEFAULT_PATH):
        configs = LocalProperties(properties_path)
        DbConnector.path = configs.get("DB_PATH")
        self.db_connector = DbConnector()

    def get_arrests_for_last_year(self, year: int = LAST_YEAR):
        stmt = select(ArrestModel).where(
            ArrestModel.arrest_date.between(date(year, 1, 1), date(year + 1, 1, 1))).order_by(
            ArrestModel.arrest_date)
        results = self.db_connector.read(lambda sess: sess.scalars(stmt).all())
        return results

    def get_arrests(self, refs: List):
        stmt = select(ArrestModel).where(ArrestModel.ref.in_(refs)).order_by(ArrestModel.arrest_date)
        results = self.db_connector.read(lambda sess: sess.scalars(stmt).all())
        return results

    def get_arrest(self, ref: int):
        stmt = select(ArrestModel).where(ArrestModel.ref.is_(ref))
        result = self.db_connector.read(lambda sess: sess.scalars(stmt).one())
        return result

    def add_arrest(self, arrest: ArrestModel):
        self.db_connector.execute(lambda sess: sess.add(arrest))

    def add_arrests(self, arrests):
        self.db_connector.execute(lambda sess: sess.add_all(arrests))

    def delete_arrests(self, arrests: List[ArrestModel]):
        for arrest in arrests:
            self.db_connector.execute(lambda sess: sess.delete(arrest))

    @staticmethod
    def _as_arrest2(result_arrest):
        print(result_arrest)
        return Arrest(result_arrest[0], None, datetime.strptime(result_arrest[1], '%Y-%m-%d %H:%M:%S'),
                      result_arrest[2])
