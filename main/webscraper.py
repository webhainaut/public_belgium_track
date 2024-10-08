import io
import os.path
import re
import shutil
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

from main.Arrest import Arrest
from main.Exceptions.MissingSectionException import MissingSectionException

NEW_DIRECTORY = "result/arrest/new"


class WebScraper:
    URL_LAST_MONTH = 'http://www.conseildetat.be/?lang=fr&page=lastmonth_{month}'
    URL_PUBLIC_PROCUREMENT = 'http://www.conseildetat.be/arr.php?nr={num}&l=fr'

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

        results = self.extract_public_procurement_infos(public_procurements_text)
        return results

    def extract_public_procurement_infos(self, public_procurements_text):
        results = []
        for public_text in public_procurements_text:
            text_result = {Arrest.REF: self.extract_ref(public_text.text),
                           Arrest.CONTRACT_TYPE: self.extract_contract_type(public_text.text),
                           Arrest.PUBLISH_DATE: self.extract_publish_date(public_text.text)}
            results.append(text_result)
        return results

    @staticmethod
    def extract_contract_type(public_text):
        # Extraire la description entre parenthèses
        description_match = re.search(r'\((.*?)\)', public_text)
        return description_match.group(1) if description_match else None

    @staticmethod
    def extract_publish_date(public_text):
        # Extraire la date entre crochets
        date_match = re.search(r'\[Ajouté le (\d{2}/\d{2}/\d{4})]', public_text)
        return date_match.group(1) if date_match else None

    @staticmethod
    def extract_ref(public_text):
        # Extract ref
        ref_match = re.search(r'\b(\d+)\b', public_text)
        return ref_match.group(1) if ref_match else None

    @staticmethod
    def clean_new_directory():
        if os.path.exists(NEW_DIRECTORY):
            shutil.rmtree(NEW_DIRECTORY)
        os.makedirs(NEW_DIRECTORY)

    @staticmethod
    def add_to_new(num, pdf):
        file_path = "{directory}/{num}.pdf".format(directory=NEW_DIRECTORY, num=num)
        with open(file_path, mode="wb") as file:
            file.write(pdf)

    def find_public_procurement(self, num, year):
        """get pdf to the public procurement for num xxxxxx"""
        directory = "result/arrest/{year}".format(year=year)
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = "{directory}/{num}.pdf".format(directory=directory, num=num)
        if not os.path.isfile(file_path):
            pdf = self.requests.get(WebScraper.URL_PUBLIC_PROCUREMENT.format(num=num)).content
            print("download : {num}.pdf".format(num=num))
            with open(file_path, mode="wb") as file:
                file.write(pdf)
            self.add_to_new(num, pdf)
            return PdfReader(io.BytesIO(pdf))
        else:
            return PdfReader(file_path)

    def extract_arrets_year(self, year, last_arrest=None):
        arrests = []
        last_month = 1
        last_ref = 1
        if last_arrest is not None:
            last_month = last_arrest.publish_date.month
            last_ref = last_arrest.ref
        months = self.get_months_order(last_month)
        for month in months:
            try:
                for dic in self.get_public_procurements_number_list(month):
                    if last_ref < int(dic[Arrest.REF]):
                        arrest = self.find_one(int(dic[Arrest.REF]), dic[Arrest.PUBLISH_DATE],
                                               dic[Arrest.CONTRACT_TYPE], year)
                        if arrest.arrest_date is None or arrest.arrest_date.year == year:
                            arrests.append(arrest)
            except MissingSectionException as e:
                print(f"{e}")
        return arrests

    def find_one(self, ref, publish_date="1/1/1900", contract_type="/", year=1900):
        pdf_reader = self.find_public_procurement(ref, year)
        arrest = Arrest(ref, pdf_reader, datetime.strptime(publish_date, '%d/%m/%Y'),
                        contract_type).find_all()
        return arrest

    def extract_arrets_list(self, refs, last_arrest=None):
        arrests = []
        filtered_refs = refs
        filtered_refs.sort()
        if last_arrest is not None:
            filtered_refs = filter(lambda ref_filter: ref_filter > last_arrest.ref, filtered_refs)
        for ref in filtered_refs:
            arrest = self.find_one(ref)
            arrests.append(arrest)
        return arrests

    @staticmethod
    def get_months_order(last_month=1):
        """ Change order off the months with last_month the first """
        all_months = [str(i).zfill(2) for i in range(1, 13)]
        months_order = all_months[last_month - 1:]
        months_order.extend(all_months[:last_month - 1])
        return months_order
