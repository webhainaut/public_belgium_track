import io
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

from Arrest import Arrest


class WebScraper:
    URL_LAST_MONTH = 'http://www.conseildetat.be/?lang=fr&page=lastmonth_{month}'
    URL_PUBLIC_PROCUREMENT = 'http://www.conseildetat.be/arr.php?nr={num}&l=fr'
    SEARCH_YEAR = datetime.now().year
    # TODO test with one month
    MONTHS = ["04"]  # ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

    def __init__(self):
        self.requests = requests

    def get_public_procurements_number_list(self, month):
        """get public procurements number list for a month"""
        response_last_month = self.requests.get(WebScraper.URL_LAST_MONTH.format(month=month))
        html_last_month = response_last_month.content
        soup_last_month = BeautifulSoup(html_last_month, 'html.parser')
        # "Marchés et travaux publics"
        # TODO remove print
        print(soup_last_month)
        public_procurements_text = soup_last_month.find_all(string=re.compile("Marchés et travaux publics"))
        print(public_procurements_text)
        public_procurements = [re.findall('[0-9]+', public_text)[0] for public_text in public_procurements_text]
        return public_procurements

    def find_public_procurement(self, num):
        """get pdf to the public procurement for num xxxxxx"""
        response_public_procurement = self.requests.get(WebScraper.URL_PUBLIC_PROCUREMENT.format(num=num))
        pdf = response_public_procurement.content
        return PdfReader(io.BytesIO(pdf))

    def find_one(self, num):
        print("Traitement de {num}".format(num=num))
        pdf_reader = self.find_public_procurement(num)
        return Arrest(num, pdf_reader).is_rectified().find_date()

    def extract_arrets(self, year=SEARCH_YEAR):
        arrests = []
        for month in WebScraper.MONTHS:
            for num in self.get_public_procurements_number_list(month):
                arrest = self.find_one(num)
                if arrest.date.year == year:
                    arrests.append(arrest)
        return arrests
