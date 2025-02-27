from sqlalchemy import select

from main.Models.Models import CaseModel
from main.dao.db_connector import DbConnector


class CaseDao:

    def __init__(self):
        self.db_connector = DbConnector()
        self.session = self.db_connector.Session()

    def get(self, roles_number: str):
        stmt = select(CaseModel).where(CaseModel.numRole.is_(roles_number))
        result = self.db_connector.read(lambda sess: sess.scalars(stmt).one(), session=self.session)
        return result
