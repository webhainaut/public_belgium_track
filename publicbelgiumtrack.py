import locale

import pandas as pd

from webscraper import WebScraper

locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')


class PublicBelgiumTrack:

    def __init__(self):
        self.pd = pd

    def write_to_excel(self, arrests):
        df = self.pd.DataFrame([arrest.as_dict() for arrest in arrests])
        df.to_excel("result/2023_Marchés et travaux publics.xlsx", sheet_name="Sheet1")


def main():
    webscraper = WebScraper()
    arrests = webscraper.extract_arrets(2023)
    public_belgium_track = PublicBelgiumTrack()
    public_belgium_track.write_to_excel(arrests)


if __name__ == "__main__":
    main()
