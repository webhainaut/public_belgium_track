import locale
from datetime import datetime, date
from typing import List

from sqlalchemy import select, exists, delete, and_, inspect

from main.Models.Models import ArrestModel
from main.dao.db_connector import DbConnector

locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')
LAST_YEAR = datetime.now().year - 1


class ArrestDao:

    def __init__(self):
        self.db_connector = DbConnector()
        self.session = self.db_connector.Session()

    def get_all(self, refs: List):
        stmt = select(ArrestModel).where(ArrestModel.ref.in_(refs)).order_by(ArrestModel.arrest_date)
        results = self.db_connector.read(lambda sess: sess.scalars(stmt).all(), session=self.session)
        return results

    def get(self, ref: int):
        stmt = select(ArrestModel).where(ArrestModel.ref.is_(ref))
        result = self.db_connector.read(lambda sess: sess.scalars(stmt).one(), session=self.session)
        return result

    def get_last(self):
        result = self.db_connector.read(lambda sess: sess.query(ArrestModel).order_by(ArrestModel.ref.desc()).first(),
                                        session=self.session)
        return result
        pass

    def exist(self, ref: int):
        stmt = exists().where(ArrestModel.ref.is_(ref))
        result = self.db_connector.read(lambda sess: sess.query(stmt).scalar(), session=self.session)
        return result

    def add(self, arrest: ArrestModel):
        arrest.cases = [self.session.merge(case) for case in arrest.cases]
        self.db_connector.execute(lambda sess: sess.add(arrest), arrest.ref, session=self.session)

    def add_all(self, arrests: List[ArrestModel]):
        self.db_connector.execute(lambda sess: sess.add_all(arrests), [arrest.ref for arrest in arrests],
                                  session=self.session)

    def delete_all(self, refs: List[int]):
        stmt = delete(ArrestModel).where(ArrestModel.ref.in_(refs))
        self.db_connector.execute(lambda sess: sess.execute(stmt), refs, session=self.session)

    def delete(self, arrest: ArrestModel):
        self.db_connector.execute(lambda sess: sess.delete(arrest), arrest.ref, session=self.session)

    def update(self, arrest: ArrestModel) -> ArrestModel:
        """
        Update the arrest with values from the new arrest.
        arrest (ArrestModel): The new arrest with updated values
        Returns:
        ArrestModel: The updated arrest
        """
        current_arrest = self.get(arrest.ref)
        # Get all column names of the ArrestModel
        columns = inspect(ArrestModel).columns.keys()

        # Update each column except 'ref'
        for column in columns:
            if column != 'ref':
                setattr(current_arrest, column, getattr(arrest, column))

        # Handle relationships separately if needed
        arrest_merge = self.session.merge(arrest)
        current_arrest.procedures = arrest_merge.procedures
        current_arrest.rulings = arrest_merge.rulings
        current_arrest.keywords = arrest_merge.keywords
        current_arrest.cases = arrest_merge.cases
        current_arrest.errors = arrest_merge.errors

        self.session.commit()
        return current_arrest

    def search_refs_and(self, **kwargs):
        query = select(ArrestModel.ref)
        conditions = []
        for attr, value in kwargs.items():
            if hasattr(ArrestModel, attr):
                if isinstance(value, list):
                    conditions.append(getattr(ArrestModel, attr).in_(value))
                else:
                    conditions.append(getattr(ArrestModel, attr).is_(value))
            else:
                raise ValueError(f"Invalid parameter value: {attr}={value}")
        if conditions:
            query = query.filter(and_(*conditions))
        return self.db_connector.read(lambda sess: sess.execute(query).scalars().all(), session=self.session)

    def search_arrests_for_year(self, year: int = LAST_YEAR):
        stmt = select(ArrestModel).where(
            ArrestModel.arrest_date.between(date(year, 1, 1), date(year + 1, 1, 1))).order_by(
            ArrestModel.arrest_date)
        results = self.db_connector.read(lambda sess: sess.scalars(stmt).all(), session=self.session)
        return results
