import re
from datetime import datetime
from enum import Enum

from main.Exceptions.DataNotFoundException import DataNotFoundException


class Arrest:
    RECTIFIED = 'Rectifié'
    PUBLISH_DATE = 'Date publication'
    ARREST_DATE = 'Date de l\'arrêt'
    CONTRACT_TYPE = 'Type de contrat'
    REF = 'Réf.'
    ASK_PROCESS = 'Demande de procédure'  # <> Procédure traitée -> voir Article 1er last page (ou presque - si "Les
    # dépens ... sont réservés" => procédure continue et dons annulation pas traitée et ou indemnité réparatrice ?.)
    PROCESS_HANDLED = 'Procédure traitée' # TODO

    def __init__(self, ref, reader, publish_date, contract_type):
        self.rectified = False
        self.publish_date = publish_date
        self.reader = reader
        self.ref = ref
        self.contract_type = contract_type
        self.arrest_date = None
        self.procedures = None

    @classmethod
    def from_dic(cls, dic):
        arrest = cls(ref=dic[cls.REF], reader=None, publish_date=dic[cls.PUBLISH_DATE],
                     contract_type=dic[cls.CONTRACT_TYPE])
        arrest.arrest_date = dic[cls.ARREST_DATE]
        arrest.rectified = dic[cls.RECTIFIED]
        arrest.procedures = [Process[chaine.strip()] for chaine in dic[cls.ASK_PROCESS].split(",")]
        return arrest

    def find_arrest_date(self):
        """find the date of arrest
        Attention quand plusieurs espace
        des fois, 1er ...
        parfois n\n o
        """
        index_page = 0 if not self.rectified else 1
        try:
            date_line = re.findall(r'(n\s*o\s.*\sdu\s\d{1,2}.*\s\d{4})', self.reader.pages[index_page].extract_text())[
                0]
        except IndexError:
            raise DataNotFoundException(data=self.ARREST_DATE, ref=self.ref)
        date_line_clean = " ".join(date_line.split()).replace('1er', '1')
        self.arrest_date = datetime.strptime(re.findall(r'(\d{1,2} \w* \d{4}$)', date_line_clean)[0], '%d %B %Y')
        return self

    def find_process(self):
        """
        si suspension / annulation / indemnité réparatrice / une combinaison
        """
        first_delimiter_pattern = re.compile(r'I\.\s*Objets*\s*(de\s*la|de\s*s|du)\s*(requête|recours)', re.IGNORECASE)
        second_delimiter_pattern = re.compile(r'II\.\s*Procédure', re.IGNORECASE)
        index_page = 0 if not self.rectified else 1

        try:

            text = self.reader.pages[index_page].extract_text()

            # Vérifier si le premier délimiteur est présent dans le texte
            if first_delimiter_pattern.search(text) is None:
                index_page = index_page + 1
                text = self.reader.pages[index_page].extract_text()
            if first_delimiter_pattern.search(text) is not None:

                # Utiliser une boucle pour rechercher le deuxième délimiteur
                while second_delimiter_pattern.search(text) is None:
                    index_page += 1
                    text += self.reader.pages[index_page].extract_text()

                # Extraire le texte entre les délimiteurs
                intern_text = self.extract_text_between_delimiters(text, first_delimiter_pattern,
                                                                   second_delimiter_pattern)
                # Appliquer la recherche des processus dans le texte interne
                self.procedures = self.search_process_in_text(intern_text)

            else:
                raise DataNotFoundException(data=self.ASK_PROCESS, ref=self.ref, message="first delimiter not found")

        except IndexError:
            raise DataNotFoundException(data=self.ASK_PROCESS, ref=self.ref)

        return self

    def extract_text_between_delimiters(self, text, first_delimiter_pattern, second_delimiter_pattern):
        pattern_delimiter = re.compile(first_delimiter_pattern.pattern + r'(.*?)' + second_delimiter_pattern.pattern,
                                       re.DOTALL)
        match = pattern_delimiter.search(text)

        if match:
            return match.group(0).strip()
        else:
            raise DataNotFoundException(data=self.ASK_PROCESS, ref=self.ref, message="Delimiters not found in text")

    @staticmethod
    def search_process_in_text(text):
        return [item for item in Process if re.search(item.value, text, re.IGNORECASE)]

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
                self.RECTIFIED: self.rectified.real,
                self.ASK_PROCESS: ', '.join([process.name for process in self.procedures])}


class Process(Enum):
    SUSPENSION = (r"((d\s*e\s*m\s*a\s*n\s*d\s*e)|(s\s*o\s*l\s*l\s*i\s*c\s*i\s*t\s*e)|(p\s*o\s*u\s*r\s*s\s*u\s*i\s*t)|("
                  r"r\s*e\s*c\s*o\s*u\s*r\s*s)).*\W*.*((l\s*a)|(d\s*e)|("
                  r"e\s*n))\s*s\s*u\s*s\s*p\s*e\s*n\s*s\s*i\s*o\s*n")
    ANNULATION = (r"(?!(.*s\s*u\s*i\s*t\s*e\s*à\s*l\s*('|’)\s*a\s*n\s*n\s*u\s*l\s*a\s*t\s*i\s*o\s*n))(?=((("
                  r"d\s*e\s*m\s*a\s*n\s*d\s*e)|(s\s*o\s*l\s*l\s*i\s*c\s*i\s*t\s*e)|("
                  r"r\s*e\s*q\s*u\s*ê\s*t\s*e))\s*\W*.*\W*\s*((l\s*('|’))|("
                  r"e\s*n))\s*a\s*n\s*n\s*u\s*l\s*a\s*t\s*i\s*o\s*n)|(d\s*('|’)\s*a\s*u\s*t\s*r\s*e\s*p\s*a\s*r\s*t,"
                  r"\s*l\s*('|’)\s*a\s*n\s*n\s*u\s*l\s*a\s*t\s*i\s*o\s*n))")
    REPARATION = (r"((d\s*e\s*m\s*a\s*n\s*d\s*e)|(s\s*o\s*l\s*l\s*i\s*c\s*i\s*t\s*e)).*\W*.*i\s*n\s*d\s*e\s*m\s*n\s*i"
                  r"\s*t\s*é\s*r\s*é\s*p\s*a\s*r\s*a\s*t\s*r\s*i\s*c\s*e")
    # Même chose que ci-dessus mais en lisible si besoin de reprendre pour modification.
    # SUSPENSION = r"((demande)|(sollicite)|(poursuit)|(recours)).*\W*.*((la)|(de)|(en))\s*suspens\s*ion"
    # ANNULATION = r"(?!(.*suite\s*à\s*l\s*('|’)\s*annulation))(?=(((demande)|(sollicite)|(requête))\W*.*\W*((l\s*('|’))|(en))\s*annu\s*lation)|(d\s*('|’)\s*autre\s*part,\s*l\s*('|’)\s*annulation))"
    # REPARATION = r"((demande)|(sollicite)).*\W*.*indemnité\s*répara\s*trice"
