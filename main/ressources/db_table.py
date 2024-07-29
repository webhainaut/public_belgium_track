from main.dao.db_connector import DbConnector
from main.dao.local_properties_dao import LocalProperties


class DbTable:

    def __init__(self, properties: LocalProperties):
        self.db_connector = DbConnector(properties.get("DB_PATH"))

    def create_arrests_table(self):
        self.db_connector.create_connection()

        create_arrest_table = """
        CREATE TABLE IF NOT EXISTS arrests (
          ref INTEGER NOT NULL PRIMARY KEY,
          publish_date TEXT,
          contract_type TEXT
        );
        """
        self.db_connector.execute_query(create_arrest_table)
        self.db_connector.close_connection()


if __name__ == "__main__":
    properties = LocalProperties()
    db_table = DbTable(properties)
    db_table.create_arrests_table()
