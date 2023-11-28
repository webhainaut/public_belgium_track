import locale

import pandas as pd

import web_scraper

locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')


def write_to_excel(arrests):
    df = pd.DataFrame([arrest.as_dict() for arrest in arrests])
    df.to_excel("result/2023_Marchés et travaux publics.xlsx", sheet_name="Sheet1")


def main():
    arrests = web_scraper.extract_arrets()
    write_to_excel(arrests)


if __name__ == "__main__":
    main()
