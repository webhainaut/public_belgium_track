from main.models.modelsDao import BaseModelDao
from main.dao.db_connector import DbConnector


class DbTable:

    def __init__(self):
        self.db_connector = DbConnector()
        self.db_connector.set_path(self.db_connector.path)

    def create_arrests_table(self):
        BaseModelDao.metadata.drop_all(self.db_connector.engine)
        BaseModelDao.metadata.create_all(self.db_connector.engine)
