import re
from enum import Enum

from main.Exceptions.DataNotFoundException import DataNotFoundException
from main.arrest_finder.FinderAbstract import FinderAbstract


class AskProcessFinder(FinderAbstract):
    """
    si suspension / annulation / indemnité réparatrice / une combinaison
    """

    def __check_args_contains(self, args):
        self.args_contain_is_rectified(args)

    def __find_data(self, ref, reader, args=None):
        index_page = self.__get_first_page(args)
        first_delimiter_pattern = re.compile(self.FIRST_TITLE_PATTERN, re.IGNORECASE)
        second_delimiter_pattern = re.compile(r'II\.\s*Procédure', re.IGNORECASE)

        try:

            text = reader.pages[index_page].extract_text()

            # Vérifier si le premier délimiteur est présent dans le texte
            if first_delimiter_pattern.search(text) is None:
                index_page = index_page + 1
                text = reader.pages[index_page].extract_text()
            if first_delimiter_pattern.search(text) is not None:

                # Utiliser une boucle pour rechercher le deuxième délimiteur
                while second_delimiter_pattern.search(text) is None:
                    index_page += 1
                    text += reader.pages[index_page].extract_text()

                # Extraire le texte entre les délimiteurs
                intern_text = self.extract_text_between_delimiters_1(ref, text, first_delimiter_pattern,
                                                                     second_delimiter_pattern)
                # Appliquer la recherche des processus dans le texte interne
                procedures = self.search_process_in_text(intern_text)

            else:
                raise DataNotFoundException(data=self.label, ref=ref, message="first delimiter not found")

        except IndexError:
            raise DataNotFoundException(data=self.label, ref=ref)
        return procedures

    @staticmethod
    def search_process_in_text(text):
        return [item for item in Process if item.is_in(text)]


class Process(Enum):
    SUSPENSION = ("Suspension",
                  r"((d\s*e\s*m\s*a\s*n\s*d\s*e)|(s\s*o\s*l\s*l\s*i\s*c\s*i\s*t\s*e)|(p\s*o\s*u\s*r\s*s\s*u\s*i\s*t)|("
                  r"r\s*e\s*c\s*o\s*u\s*r\s*s)).*\W*.*((l\s*a)|(d\s*e)|("
                  r"e\s*n))\s*s\s*u\s*s\s*p\s*e\s*n\s*s\s*i\s*o\s*n")
    ANNULATION = ("Annulation",
                  r"(?!(.*s\s*u\s*i\s*t\s*e\s*à\s*l\s*('|’)\s*a\s*n\s*n\s*u\s*l\s*a\s*t\s*i\s*o\s*n))(?=((("
                  r"d\s*e\s*m\s*a\s*n\s*d\s*e)|(s\s*o\s*l\s*l\s*i\s*c\s*i\s*t\s*e)|("
                  r"r\s*e\s*q\s*u\s*ê\s*t\s*e))\s*\W*.*\W*\s*((l\s*('|’))|("
                  r"e\s*n))\s*a\s*n\s*n\s*u\s*l\s*a\s*t\s*i\s*o\s*n)|(d\s*('|’)\s*a\s*u\s*t\s*r\s*e\s*p\s*a\s*r\s*t,"
                  r"\s*l\s*('|’)\s*a\s*n\s*n\s*u\s*l\s*a\s*t\s*i\s*o\s*n))")
    REPARATION = ("Réparation",
                  r"((d\s*e\s*m\s*a\s*n\s*d\s*e)|(s\s*o\s*l\s*l\s*i\s*c\s*i\s*t\s*e)).*\W*.*i\s*n\s*d\s*e\s*m\s*n\s*i"
                  r"\s*t\s*é\s*r\s*é\s*p\s*a\s*r\s*a\s*t\s*r\s*i\s*c\s*e")

    def __init__(self, label, pattern):
        self.label = label
        self.pattern = pattern

    def is_in(self, text):
        return re.search(self.pattern, text, re.IGNORECASE)

    # Même chose que ci-dessus mais en lisible si besoin de reprendre pour modification.
    # SUSPENSION = r"((demande)|(sollicite)|(poursuit)|(recours)).*\W*.*((la)|(de)|(en))\s*suspens\s*ion"
    # ANNULATION = r"(?!(.*suite\s*à\s*l\s*('|’)\s*annulation))(?=(((demande)|(sollicite)|(requête))\W*.*\W*((l\s*('|’))|(en))\s*annu\s*lation)|(d\s*('|’)\s*autre\s*part,\s*l\s*('|’)\s*annulation))"
    # REPARATION = r"((demande)|(sollicite)).*\W*.*indemnité\s*répara\s*trice"
