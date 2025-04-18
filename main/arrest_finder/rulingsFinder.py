import re
from enum import Enum
from typing import List

from pypdf import PdfReader

from main.exceptions.dataNotFoundException import DataNotFoundException
from main.models.modelsDao import RulingModelDao
from main.arrest_finder.finderAbstract import FinderAbstract
from main.arrest_finder.finderService import FinderService

# surplus_delimiter = r"\s*pour\s*le\s*surplus"
SURPLUS_DELIMITER = r"\s*p\s*o\s*u\s*r\s*l\s*e\s*s\s*u\s*r\s*p\s*l\s*u\s*s"


class RulingsFinder(FinderAbstract, FinderService):
    """Quel est la décision"""

    def _check_args_contains(self, args):
        self.args_contain_is_rectified(args)

    def _find_data(self, ref, reader: PdfReader, args=None):
        if args[self.IS_RECTIFIED_LABEL]:
            return []

        try:
            first_delimiter_pattern = self.RULING_PATTERN
            second_delimiter_pattern = r"(e\s*x\s*é\s*c\s*u\s*t\s*i\s*o\s*n\s*i\s*m\s*m\s*é\s*d\s*i\s*a\s*t\s*e)"
            text = self.extract_text_between_delimiters_for_reader(self.service, ref, reader, first_delimiter_pattern,
                                                                   second_delimiter_pattern, strict=False,
                                                                   reverse_1=True)
            rulings = self.search_ruling_in_text(text, ref)
        except IndexError:
            raise DataNotFoundException(data=self.service, ref=ref)
        return rulings

    def is_rectified_ruling(self, reader, ref):
        try:
            self.extract_text_between_delimiters_for_reader(self.service, ref, reader, Ruling.RECTIFIED.pattern)
        except DataNotFoundException:
            return False
        return True

    def search_ruling_in_text(self, text, ref):
        rulings: List[RulingModelDao] = []
        for item in Ruling:
            if item.is_in(text):
                surplus = item.is_suplus(text)
                rulings.append(RulingModelDao(ruling=item.label, surplus=surplus))
        if len(rulings) < 1:
            raise DataNotFoundException(data=self.service, ref=ref)
        return rulings


class Ruling(Enum):
    LIFT = ("Levée", r"e\s*s\s*t\s*l\s*e\s*v\s*é", None)
    RECTIFIED = ("Rectifier", r"A\s*R\s*R\s*Ê\s*T\s*R\s*E\s*C\s*T\s*I\s*F\s*I\s*C\s*A\s*T\s*I\s*F", None)
    REJECT = ("Rejeter", r"(?!(r\s*e\s*q\s*u\s*ê\s*t\s*e\s*e\s*n\s*i\s*n\s*t\s*e\s*r"
                         r"\s*v\s*e\s*n\s*t\s*i\s*o\s*n))(?=((("
                         r"d\s*e\s*m\s*a\s*n\s*d\s*e)|(r\s*e\s*q\s*u\s*ê\s*t\s*e)|("
                         r"r\s*e\s*c\s*o\s*u\s*r\s*s)).*r\s*e\s*j\s*e\s*t\s*(é|e)e?))",
              r'r\s*e\s*j\s*e\s*t\s*(é|e)e?' + SURPLUS_DELIMITER)
    CANCELLED = ("Annulée", r"((e\s*s\s*t)|(s\s*o\s*n\s*t))\s*a\s*n{,2}\s*u\s*l\s*é\s*e", None)
    ISSUES_DECREE = ("Décrète le désistement",
                     r"d\s*é\s*s\s*i\s*s\s*t\s*e\s*m\s*e\s*n\s*t\s*.*\s*d\s*é\s*c\s*r\s*é\s*t\s*é", None)
    ACKNOWLEDGE_DECREE = ("Acte le désistement", r"((d\s*é\s*s\s*i\s*s\s*t\s*e\s*m\s*e\s*n\s*t.*e\s*s\s*t\s*a\s*c\s*t"
                                                 r"\s*é)|("
                                                 r"a\s*c\s*t\s*e\s*d\s*u\s*d\s*é\s*s\s*i\s*s\s*t\s*e\s*m\s*e\s*n\s*t))",
                          r'd\s*é\s*s\s*i\s*s\s*t\s*e\s*m\s*e\s*n\s*t' + SURPLUS_DELIMITER)
    ORDERED = ("Ordonné", r"e\s*s\s*t\s*o\s*r\s*d\s*o\s*n{,2}é\s*e?", None)
    NO_LONGER_REQUIRED = (
    "Plus lieu de statuer", r"p\s*l\s*u\s*s\s*l\s*i\s*e\s*u\s*d\s*e\s*s\s*t\s*a\s*t\s*u\s*e\s*r", None)
    UNCOMPLETED = ("Non accomplie", r"n\s*o\s*n\s*a\s*c\s*c\s*o\s*m\s*p\s*l\s*i\s*e", None)
    SINE_DIE = ("Remise sine die", r"r\s*e\s*m\s*i\s*s\s*e\s*s\s*i\s*n\s*e\s*d\s*i\s*e", None)
    REOPENING_DEBATES = ("Reouverture des débats", r"((d\s*é\s*b\s*a\s*t\s*s?\s*((s\s*o\s*n\s*t)|("
                                                   r"e\s*s\s*t))\s*r\s*o\s*u\s*v\s*e\s*r\s*t)|("
                                                   r"r\s*e\s*o\s*u\s*v\s*e\s*r\s*t\s*u\s*r\s*e\s*((d\s*e\s*s)|("
                                                   r"d\s*u))\s*d\s*é\s*b\s*a\s*t))", None)
    NOT_FOUND = ("NOT FOUND", "$$$$$$$$$$$$$$$$$$$$$$$$$$$NOT FOUND$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", None)
    BIFFEE = ("Biffée", "affaire est biffée du rôle", None)  ## TODO compléter
    ACORDEE = ("Acordée", "indemnité réparatrise accordée", None)  ## TODO compléter

    def __init__(self, label, pattern, surplus_pattern):
        self.label = label
        self.pattern = pattern
        self.surplus_pattern = pattern + SURPLUS_DELIMITER if surplus_pattern is None else surplus_pattern

    def is_in(self, text):
        return re.search(self.pattern, text, re.IGNORECASE + re.DOTALL)

    def is_suplus(self, text):
        return re.search(self.surplus_pattern, text, re.IGNORECASE) is not None

# REJECT = r"(?!((.*rejetée pour le surplus)|(requête\s*en\s*intervention)))(?=(((demande)|(requête)|(recours)).*rejet(é|e)))"
# REJECT = r"(?!(requête\s*en\s*intervention))(?=(((demande)|(requête)).*rejet(é|e)e?))"
# CANCELLED = r"((est)|(sont))\s*an{,2}ulée"
# ISSUES_DECREE = r"désistement\s*.*\s*décrété"
# ACKNOWLEDGE_DECREE = r"((désistement.*est\s*acté)|(acte\s*du\s*désistement))"
# UNCOMPLETED = r"non accomplie"

# ORDERED = r"e\s*s\s*t\s*o\s*r\s*d\s*o\s*n{,2}é\s*e?"
# ORDERED = r"((suspension)|(annulation)|(indemnité\s*répara\s*trice)).*e\s*s\s*t\s*o\s*r\s*d\s*o\s*n{,2}é\s*e?"
# REOPENING_DEBATES = r"((débats?\s*((sont)|(est))\s*rouvert)|(reouverture\s*((des)|(du))\s*débat))"
