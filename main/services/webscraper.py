import logging
import re

import requests
from bs4 import BeautifulSoup

from main.Exceptions.MissingSectionException import MissingSectionException

NEW_DIRECTORY = "result/arrest/new"
FILES_PATH_DOWNLOAD = "result/arrest/{year}"


class WebScraper:
    """
    Find the arrests to the site
    """
    URL_LAST_MONTH = 'http://www.conseildetat.be/?lang=fr&page=lastmonth_{month}'
    URL_PUBLIC_PROCUREMENT = 'http://www.conseildetat.be/arr.php?nr={ref}'

    def __init__(self):
        self.requests = requests
        self.logger = logging.getLogger(__name__)

    def find_arrest(self, ref):
        procurement_url = WebScraper.URL_PUBLIC_PROCUREMENT.format(ref=ref)
        response = self.requests.get(procurement_url)
        if response.status_code != 200:
            raise Exception(
                "Code error {status} on page {url}".format(status=response.status_code, url=procurement_url))
        elif response.headers.get('Content-Type') != "application/pdf":
            raise Exception(
                f"Arrest '{ref}' not found Content-Type '{response.headers.get('Content-Type')}' : {response.content}")
        return response.content

    def find_arrests(self, refs):
        pdfs = []
        for ref in refs:
            pdfs.append(self.find_arrest(ref))
        return pdfs

    def find_public_procurements_refs(self, last_month=1, last_ref:int=None):
        refs = []
        if last_month is None or last_month < 1:
            last_month=1
        months = self.get_months_order(last_month)
        for month in months:
            try:
                refs = refs + self.find_public_procurements_refs_month(month, last_ref)
            except MissingSectionException as e:
                self.logger.error(f"{e}")
        return refs

    def find_public_procurements_refs_month(self, month, last_ref: int=None):
        """retourne une liste des refs des arrets du mois month"""
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
        public_procurements_balise = arrest_section.findNext('ul').findAll('li')
        refs = self.extract_public_procurement_refs(public_procurements_balise, last_ref)
        return refs

    def extract_public_procurement_refs(self, public_procurements_text, last_ref=None):
        results = []
        for public_text in public_procurements_text:
            ref = self.extract_ref(public_text.text)
            if last_ref is None or ref > last_ref:
                results.append(ref)
        return results

    @staticmethod
    def extract_ref(public_text):
        # Extract ref
        ref_match = re.search(r'\b(\d+)\b', public_text)
        return int(ref_match.group(1)) if ref_match else None

    @staticmethod
    def get_months_order(last_month=1):
        """ Change order off the months with last_month the first """
        all_months = [str(i).zfill(2) for i in range(1, 13)]
        months_order = all_months[last_month - 1:]
        months_order.extend(all_months[:last_month - 1])
        return months_order
