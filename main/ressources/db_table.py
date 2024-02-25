from main.dao.db_connector import DbConnector
from main.dao.local_properties_dao import LocalProperties

configs = LocalProperties()


db_connector = DbConnector(configs.get("DB_PATH"))
db_connector.create_connection()

create_arrest_table = """
CREATE TABLE IF NOT EXISTS arrests (
  ref INTEGER NOT NULL PRIMARY KEY,
  publish_date TEXT,
  contract_type TEXT
);
"""
db_connector.execute_query(create_arrest_table)

db_connector.close_connection()

# create_users = """
# INSERT INTO
#   users (name, age, gender, nationality)
# VALUES
#   ('James', 25, 'male', 'USA'),
#   ('Leila', 32, 'female', 'France'),
#   ('Brigitte', 35, 'female', 'England'),
#   ('Mike', 40, 'male', 'Denmark'),
#   ('Elizabeth', 21, 'female', 'Canada');
# """
#
# execute_query(connection, create_users)
