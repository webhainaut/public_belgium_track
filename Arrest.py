import re
from datetime import datetime

from Exceptions.DataNotFoundException import DataNotFoundException


class Arrest:
    RECTIFIED = 'Rectifié'
    PUBLISH_DATE = 'Date publication'
    ARREST_DATE = 'Date de l\'arrêt'
    CONTRACT_TYPE = 'Type de contrat'
    REF = 'Réf.'

    def __init__(self, ref, reader, publish_date, contract_type):
        self.rectified = False
        self.publish_date = publish_date
        self.reader = reader
        self.ref = ref
        self.contract_type = contract_type
        self.arrest_date = None

    @classmethod
    def from_dic(cls, dic):
        arrest = cls(ref=dic[cls.REF], reader=None, publish_date=dic[cls.PUBLISH_DATE],
                     contract_type=dic[cls.CONTRACT_TYPE])
        arrest.arrest_date = dic[cls.ARREST_DATE]
        arrest.rectified = dic[cls.RECTIFIED]
        return arrest

    def find_arrest_date(self):
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
        try:
            date_line = re.findall(r'(n\s*o\s.*\sdu\s\d{1,2}.*\s\d{4})', self.reader.pages[index_page].extract_text())[
                0]
        except IndexError:
            raise DataNotFoundException(data="date", ref=self.ref)
        date_line_clean = " ".join(date_line.split()).replace('1er', '1')
        self.arrest_date = datetime.strptime(re.findall(r'(\d{1,2} \w* \d{4}$)', date_line_clean)[0], '%d %B %Y')
        return self

    def is_rectified(self):
        self.rectified = re.search(r'(arrêt n.* du .* est rectif.* par .*arrêt n.* du .*)',
                                   self.reader.pages[0].extract_text()) is not None
        return self

    def format_date(self):
        if self.publish_date is not None:
            return self.publish_date.strftime("%d/%m/%Y")

    def as_dict(self):
        return {self.REF: self.ref, self.PUBLISH_DATE: self.publish_date, self.CONTRACT_TYPE: self.contract_type,
                self.ARREST_DATE: self.arrest_date,
                self.RECTIFIED: self.rectified.real}
