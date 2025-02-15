from main.dao.db_connector import DbConnector
from main.Models.Models import BaseModel


class DbTable:

    def __init__(self):
        self.db_connector = DbConnector()
        self.db_connector.set_path(self.db_connector.path)

    def create_arrests_table(self):
        BaseModel.metadata.drop_all(self.db_connector.engine)
        BaseModel.metadata.create_all(self.db_connector.engine)
