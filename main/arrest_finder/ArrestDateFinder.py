import re
from datetime import datetime

from main.Exceptions.DataNotFoundException import DataNotFoundException
from main.arrest_finder.FinderAbstract import FinderAbstract
from main.arrest_finder.FinderService import FinderService



class ArrestDateFinder(FinderAbstract, FinderService):
    """
    Trouve la date de l'arrêt.
    Gère les cas particuliers comme les espaces multiples, '1er', et 'n\n o'.
    """

    ARREST_DATE_PATTERN = r'(n\s*o\s*[\d.,]+\s*(?:du)?\s*\d{1,2}(?:er)?\s*[\wé]+\s*\d{4})'

    def _check_args_contains(self, args):
        self.args_contain_is_rectified(args)

    def _find_data(self, ref, reader, args=None):
        index_page = self._get_first_page(args)
        try:
            date_line = re.findall(self.ARREST_DATE_PATTERN, reader.pages[index_page].extract_text())[
                0]
        except IndexError:
            raise DataNotFoundException(data=self.service, ref=ref)

        date_str = self.normalize_date_string(self, date_line, ref)
        try:
            return datetime.strptime(date_str, '%d %B %Y')
        except ValueError:
            raise DataNotFoundException(data=self.service, ref=ref)
