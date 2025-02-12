import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DbConnector:
    logging.basicConfig(level=logging.ERROR)
    path = "dbs/main.db"
    db_path = os.path.abspath(os.path.dirname(__file__)) + "/../../" + path
    engine = create_engine(f"sqlite:///{db_path}", echo=True)
    Session = sessionmaker(engine)

    @classmethod
    def set_path(cls, new_path):
        cls.path = new_path
        cls.db_path = os.path.abspath(os.path.dirname(__file__)) + "/../../" + cls.path
        cls.engine = create_engine(f"sqlite:///{cls.db_path}", echo=True)
        cls.Session = sessionmaker(cls.engine)

    def read(self, func):
        session = self.Session()
        try:
            result = func(session)
            return result
        except Exception as e:
            logging.error(f"An error occurred during execution: {e}")
            return None

    def execute(self, func):
        with self.Session() as session:
            try:
                func(session)
                session.commit()
            except Exception as e:
                session.rollback()
                logging.error(f"An error occurred during execution: {e}")
