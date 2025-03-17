from sqlalchemy import select, inspect

from main.Models.ModelsDao import CaseModelDao
from main.dao.db_connector import DbConnector


class CaseDao:

    def __init__(self):
        self.db_connector = DbConnector()
        self.session = self.db_connector.Session()

    def get(self, roles_number: str):
        stmt = select(CaseModelDao).where(CaseModelDao.numRole.is_(roles_number))
        result = self.db_connector.read(lambda sess: sess.scalars(stmt).one(), session=self.session)
        return result
