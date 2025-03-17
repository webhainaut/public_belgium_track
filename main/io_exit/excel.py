import logging
import os
from typing import List

import pandas as pd
from openpyxl.styles import NamedStyle

from main.models.models import ArrestModel, REF

SHEET_NAME = 'result'

DATE_STYLE = NamedStyle(name='date_style', number_format='DD/MM/YYYY')


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
                                if_sheet_exists="overlay", ) as writer:
                df.to_excel(writer, sheet_name=SHEET_NAME, index=False, startrow=begin_line, header=False)
                self.change_excel(df, writer)

            self.logger.info("remlir a partir de {begin_line}".format(begin_line=begin_line))
        except FileNotFoundError:
            with pd.ExcelWriter(DEFAULT_PATH.format(file_name=file_name), engine='openpyxl', mode='w') as writer:
                df.to_excel(writer, sheet_name=SHEET_NAME, index=False, freeze_panes=(1, 1))
                self.change_excel(df, writer)

    def change_excel(self, df, writer):
        worksheet= writer.sheets[SHEET_NAME]
        worksheet.auto_filter.ref = worksheet.dimensions

        self.adjust_column_width(worksheet)

        self.adjust_row_height(worksheet)

        self.apply_date_style(df, worksheet, "G")

    @staticmethod
    def adjust_row_height(worksheet):
        for row in worksheet.iter_rows():
            max_ligne = 1
            for cell in row:
                nb_ligne = str(cell.value).count('\n') + 1
                if nb_ligne > max_ligne:
                    max_ligne = nb_ligne
            worksheet.row_dimensions[row[0].row].height = max_ligne * 16

    @staticmethod
    def adjust_column_width(worksheet):
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter  # Obtenir la lettre de la colonne
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = max_length + 2  # Ajouter un petit espace
            worksheet.column_dimensions[column_letter].width = adjusted_width

    @staticmethod
    def apply_date_style(df, worksheet, column):
        for row in range(2, len(df) + 2):  # Commence à 2 pour sauter l'en-tête
            if DATE_STYLE.name not in worksheet[f'{column}{row}'].style :
                worksheet[f'{column}{row}'].style = DATE_STYLE

    @staticmethod
    def get_last_line(file_name):
        if os.path.exists(DEFAULT_PATH.format(file_name=file_name)):
            df = pd.read_excel(DEFAULT_PATH.format(file_name=file_name))
            return df.index[-1] + 1
        else:
            return 0
