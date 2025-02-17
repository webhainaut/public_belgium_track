import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DbConnector:
    path = "dbs/public_belgium.db"
    db_path = os.path.abspath(os.path.dirname(__file__)) + "/../../" + path
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    Session = sessionmaker(engine)

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @classmethod
    def set_path(cls, new_path):
        cls.path = new_path
        cls.db_path = os.path.abspath(os.path.dirname(__file__)) + "/../../" + cls.path
        cls.engine = create_engine(f"sqlite:///{cls.db_path}", echo=False)
        cls.Session = sessionmaker(cls.engine)

    def read(self, func):
        session = self.Session()
        try:
            result = func(session)
            return result
        except Exception as e:
            self.logger.error(f"An error occurred during execution: {e}")
            return None

    def execute(self, func):
        with self.Session() as session:
            try:
                func(session)
                session.commit()
            except Exception as e:
                session.rollback()
                self.logger.error(f"An error occurred during execution: {e}")
