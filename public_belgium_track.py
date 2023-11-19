import io
import locale
import re
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

SEARCH_YEAR = 2023

locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')


class Arrest:
    def __init__(self, num, reader):
        self.rectified = False
        self.date = None
        self.reader = reader
        self.num = num

    def find_date(self):
        """find the date of arrest
        Attention quand lusieurs espace
        des fois, 1er ...
        parfois n\n o
        """
        # TODO gérer exception si ne trouve pas de date
        # TODO mettre dans un fichier à part si exception
        index_page = 0
        if self.rectified:
            index_page = 1
        date_line = re.findall(r'(n\s*o\s.*\sdu\s\d{1,2}.*\s\d{4})', self.reader.pages[index_page].extract_text())[0]
        date_line_clean = " ".join(date_line.split()).replace('1er', '1')
        self.date = datetime.strptime(re.findall(r'(\d{1,2} \w* \d{4}$)', date_line_clean)[0], '%d %B %Y')
        return self

    def format_number(self):
        """format the number with '.'"""
        # TODO Tester avec xx, xxx, xxxxxx, xxxxxxx, doit donner xx, xxx, xxx.xxx, x.xxx.xxx
        chunks, chunk_size = len(self.num), 3
        reverted_number = self.num[::-1]
        split = [reverted_number[i:i + chunk_size] for i in range(0, chunks, chunk_size)]
        return '.'.join(split)[::-1]

    def is_rectified(self):
        self.rectified = re.search(r'(arrêt n.* du .* est rectif.* par .*arrêt n.* du .*)',
                                   self.reader.pages[0].extract_text()) is not None
        if self.rectified:
            print("Arrêt rectifié")
        return self

    def as_dict(self):
        return {'Num': self.format_number(), 'Date': self.date.strftime("%d/%m/%Y"),
                'Rectifié': self.rectified.real}


def get_months():
    """get months MM"""
    # TODO test : return ["02"]
    # return ["02"]
    return ['{:02d}'.format(moth + 1) for moth in range(12)]


def get_public_procurements_number_list(month):
    """get public procurements number list for a month"""
    url_last_month = f'http://www.conseildetat.be/?lang=fr&page=lastmonth_{month}'
    response_last_month = requests.get(url_last_month.format(month=month))
    html_last_month = response_last_month.content
    soup_last_month = BeautifulSoup(html_last_month, 'html.parser')

    public_procurements_text = soup_last_month.find_all(string=re.compile(".*Marchés publics.*"))
    public_procurements = [re.findall('[0-9]+', public_text)[0] for public_text in public_procurements_text]
    return public_procurements


def find_public_procurement(num):
    """get pdf to the public procurement for num xxxxxx"""
    url_public_procurement = 'http://www.conseildetat.be/arr.php?nr={num}&l=fr'
    response_public_procurement = requests.get(url_public_procurement.format(num=num))
    pdf = response_public_procurement.content
    return PdfReader(io.BytesIO(pdf))


def find_all():
    arrests = []
    for month in get_months():
        for num in get_public_procurements_number_list(month):
            arrest = find_one(num)
            if arrest.date.year == SEARCH_YEAR:
                arrests.append(arrest)
    return arrests


def find_one(num):
    print("Traitement de {num}".format(num=num))
    pdf_reader = find_public_procurement(num)
    return Arrest(num, pdf_reader).is_rectified().find_date()


arrests = find_all()
df = pd.DataFrame([arrest.as_dict() for arrest in arrests])
df.to_excel("result/2023_Marchés et travaux publics.xlsx", sheet_name="Sheet1")

# find_all()
# find_one(255267)
# find_one(255470)
# find_one(255668)
# find_one(255844)
# find_one(256672)
# find_one(257478)
# find_one(247478)
