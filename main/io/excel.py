import logging
import os
from typing import List

import pandas as pd

from main.Models.Models import ArrestModel, REF

DEFAULT_PATH = "result/{file_name}.xlsx"
DEFAULT_NAME = "result"


class Excel:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.pd = pd

    def add(self, arrests: List[ArrestModel], file_name=DEFAULT_NAME):
        if file_name is None:
            file_name = DEFAULT_NAME
        begin_line = self.get_last_line(file_name) + 1
        df = self.pd.DataFrame([arrest.as_dict() for arrest in arrests])
        if not df.empty:
            df = df.sort_values(by=REF)
        try:
            with pd.ExcelWriter(DEFAULT_PATH.format(file_name=file_name), engine='openpyxl', mode='a',
                                if_sheet_exists="overlay") as writer:
                df.to_excel(writer, sheet_name='Feuille1', index=False, startrow=begin_line, header=False)
            self.logger.info("remlir a partir de {begin_line}".format(begin_line=begin_line))
        except FileNotFoundError:
            with pd.ExcelWriter(DEFAULT_PATH.format(file_name=file_name), engine='openpyxl', mode='w') as writer:
                df.to_excel(writer, sheet_name='Feuille1', index=False)

    @staticmethod
    def get_last_line(file_name):
        if os.path.exists(DEFAULT_PATH.format(file_name=file_name)):
            df = pd.read_excel(DEFAULT_PATH.format(file_name=file_name))
            return df.index[-1] + 1
        else:
            return 0
