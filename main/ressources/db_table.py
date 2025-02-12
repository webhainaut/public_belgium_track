from main.Models.BaseModel import BaseModel
from main.dao.db_connector import DbConnector
from main.dao.local_properties_dao import LocalProperties


class DbTable:

    def __init__(self, properties: LocalProperties):
        DbConnector.set_path(properties.get("DB_PATH"))
        self.db_connector = DbConnector()

    def create_arrests_table(self):
        BaseModel.metadata.drop_all(self.db_connector.engine)
        BaseModel.metadata.create_all(self.db_connector.engine)


if __name__ == "__main__":
    properties = LocalProperties()
    db_table = DbTable(properties)
    db_table.create_arrests_table()
