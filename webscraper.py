import io
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

from Arrest import Arrest
from Exceptions.MissingSectionException import MissingSectionException


class WebScraper:
    URL_LAST_MONTH = 'http://www.conseildetat.be/?lang=fr&page=lastmonth_{month}'
    URL_PUBLIC_PROCUREMENT = 'http://www.conseildetat.be/arr.php?nr={num}&l=fr'
    SEARCH_YEAR = datetime.now().year

    def __init__(self):
        self.requests = requests

    def get_public_procurements_number_list(self, month):
        """get public procurements (ref, contact type) list for a month"""
        month_format_url = WebScraper.URL_LAST_MONTH.format(month=month)
        response_last_month = self.requests.get(month_format_url)
        if response_last_month.status_code != 200:
            raise Exception(
                "Code error {status} on page {url}".format(status=response_last_month.status_code,
                                                           url=month_format_url))
        html_last_month = response_last_month.content
        soup_last_month = BeautifulSoup(html_last_month, 'html.parser')
        arrest_section = soup_last_month.find(string=re.compile("Marchés et travaux publics"))
        if not arrest_section:
            raise MissingSectionException(title="Marchés et travaux publics", url=month_format_url)
        public_procurements_text = arrest_section.findNext('ul').findAll('li')
        public_procurements = [(re.findall(r'[0-9]+', public_text.text)[0],
                                re.findall(r'\(.*\)', public_text.text)[0].replace("(", "").replace(")", ""))
                               for public_text in public_procurements_text]
        return public_procurements

    def find_public_procurement(self, num):
        """get pdf to the public procurement for num xxxxxx"""
        response_public_procurement = self.requests.get(WebScraper.URL_PUBLIC_PROCUREMENT.format(num=num))
        pdf = response_public_procurement.content
        return PdfReader(io.BytesIO(pdf))

    def find_one(self, ref):
        pdf_reader = self.find_public_procurement(ref)
        arrest = Arrest(ref, pdf_reader).is_rectified().find_date()
        print("Traitement de {num} en date du {date}".format(num=ref, date=arrest.format_date()))
        return arrest

    def extract_arrets(self, year=SEARCH_YEAR, last_arrest=None):
        arrests = []
        last_month = 1
        last_ref = 1
        if last_arrest is not None:
            last_month = last_arrest.date.month
            last_ref = last_arrest.ref
        months = self.get_months(last_month)
        for month in months:
            for (ref, contract) in self.get_public_procurements_number_list(month):
                if last_ref < int(ref):
                    arrest = self.find_one(int(ref))
                    arrest.contract_type = contract
                    if arrest.date.year == year:
                        arrests.append(arrest)
        return arrests

    @staticmethod
    def get_months(last_month=1):
        all_months = [str(i).zfill(2) for i in range(1, 13)]
        partial_months = all_months[last_month - 1:]
        return partial_months
