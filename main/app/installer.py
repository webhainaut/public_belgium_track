import locale
import os
from datetime import datetime

from main.dao.dbtable import DbTable

locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')


class Installer:

    def __init__(self):
        self.db_table = DbTable()

    def install(self):
        self.db_table.create_arrests_table()

    def db_exists(self):
        return os.path.exists(self.db_table.db_connector.db_path)


if __name__ == "__main__":
    start_time = datetime.now()
    installer = Installer()
    installer.install()
    end_time = datetime.now()
    execution_time = end_time - start_time
    print(f"Le script a pris {execution_time} secondes pour s'exécuter.")
