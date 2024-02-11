import locale
import os
from datetime import datetime

import pandas as pd
from openpyxl.reader.excel import load_workbook

from main.Arrest import Arrest
from main.webscraper import WebScraper

locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')


class PublicBelgiumTrack:
    YEAR = 2023
    # YEAR = datetime.now().year
    FILE_PATH_EXCEL_FORMAT = "result/test_CE VIe ch. {year}.xlsx"

    def __init__(self, file_path=FILE_PATH_EXCEL_FORMAT, year=YEAR):
        self.pd = pd
        self.load_workbook = load_workbook
        self.webscraper = WebScraper()
        self.file_path = file_path.format(year=year)
        self.previous_df = None
        self.begin_line = 0
        self.last_arrest = None

    def write_to_excel(self, arrests):
        df = self.pd.DataFrame([arrest.as_dict() for arrest in arrests])
        if not df.empty:
            df = df.sort_values(by=Arrest.REF)
        try:
            with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='a', if_sheet_exists="overlay") as writer:
                df.to_excel(writer, sheet_name='Feuille1', index=False, startrow=self.begin_line, header=False)
            print("remlir a partir de {begin_line} - last arrest : {arrest}".format(begin_line=self.begin_line,
                                                                                    arrest=self.last_arrest.as_dict()))
        except FileNotFoundError:
            with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='w') as writer:
                df.to_excel(writer, sheet_name='Feuille1', index=False)

    def read_from_excel(self):
        if os.path.isfile(self.file_path):
            return self.pd.read_excel(self.file_path)
        else:
            print(f"Le fichier n'existe pas.")

    def last_line(self):
        if self.previous_df is not None:
            return len(self.previous_df) + 1
        return 0

    def find_last_arrest(self):
        self.previous_df = self.read_from_excel()
        self.begin_line = self.last_line()
        self.last_arrest = self.find_last_arrest_from_previous_df()

    def find_last_arrest_from_previous_df(self):
        if self.previous_df is not None:
            return Arrest.from_dic(self.previous_df.tail(1).to_dict(orient='records')[0])

    def get_arrests(self, refs=None):
        if refs is not None:
            return self.webscraper.extract_arrets_list(refs, self.last_arrest)
        else:
            return self.webscraper.extract_arrets_year(self.YEAR, self.last_arrest)


def main():
    public_belgium_track = PublicBelgiumTrack()
    public_belgium_track.find_last_arrest()
    arrests = public_belgium_track.get_arrests(REFS)
    public_belgium_track.write_to_excel(arrests)


REFS = None
# REFS = [247478, 255267, 255438, 255470, 255472, 255668, 255678, 255679, 255681, 255844, 255962, 255964, 256014, 256484, 256672, 257478, 257654, 257819, 257919, 257921, 258204, 240250, 255824, 258274, 255681]
if __name__ == "__main__":
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    execution_time = end_time - start_time
    print(f"Le script a pris {execution_time} secondes pour s'exécuter.")
