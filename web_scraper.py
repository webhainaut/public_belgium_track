import io
import re

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

from Arrest import Arrest

SEARCH_YEAR = 2023


def get_months():
    """get months MM"""
    # TODO test : return ["02"]
    return ["02"]
    # return ['{:02d}'.format(moth + 1) for moth in range(12)]


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


def find_one(num):
    print("Traitement de {num}".format(num=num))
    pdf_reader = find_public_procurement(num)
    return Arrest(num, pdf_reader).is_rectified().find_date()


def extract_arrets():
    arrests = []
    for month in get_months():
        for num in get_public_procurements_number_list(month):
            arrest = find_one(num)
            if arrest.date.year == SEARCH_YEAR:
                arrests.append(arrest)
    return arrests
