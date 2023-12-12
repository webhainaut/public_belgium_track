import locale
import os

import pandas as pd

from Arrest import Arrest
from webscraper import WebScraper

FILE_PATH_EXCEL = "result/2023_Marchés et travaux publics.xlsx"

locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')


class PublicBelgiumTrack:

    def __init__(self):
        self.pd = pd

    def write_to_excel(self, arrests, file_path=FILE_PATH_EXCEL):
        df = self.pd.DataFrame([arrest.as_dict() for arrest in arrests])
        df.to_excel(file_path, sheet_name="Sheet1", index=False)

    def read_from_excel(self, file_path=FILE_PATH_EXCEL):
        if os.path.isfile(file_path):
            df = self.pd.read_excel(file_path)
            return Arrest.from_dic(df.tail(1).to_dict(orient='records')[0])
        else:
            print(f"Le fichier n'existe pas.")


def main():
    public_belgium_track = PublicBelgiumTrack()
    last_infos = public_belgium_track.read_from_excel(FILE_PATH_EXCEL)
    print(last_infos.ref)
    print(last_infos.date)
    webscraper = WebScraper()
    arrests = webscraper.extract_arrets(2023)
    public_belgium_track.write_to_excel(arrests, FILE_PATH_EXCEL)


if __name__ == "__main__":
    main()
