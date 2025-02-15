import locale
from datetime import datetime

from main.dao.dbtable import DbTable

locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')


def main():
    install = DbTable()
    install.create_arrests_table()


if __name__ == "__main__":
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    execution_time = end_time - start_time
    print(f"Le script a pris {execution_time} secondes pour s'exécuter.")
