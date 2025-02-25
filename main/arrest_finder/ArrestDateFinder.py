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
    DATE_EXTRACT_PATTERN = r'(\d{1,2})\s*([^\d\s]+)\s*(\d{4})'
    DATE_PATTERN = r'(\d{1,2}\s*[\wé]+\s*\d{4})'

    def _check_args_contains(self, args):
        self.args_contain_is_rectified(args)

    def _find_data(self, ref, reader, args=None):
        index_page = self._get_first_page(args)
        try:
            date_line = re.findall(self.ARREST_DATE_PATTERN, reader.pages[index_page].extract_text())[
                0]
        except IndexError:
            raise DataNotFoundException(data=self.service, ref=ref)

        date_str = self._normalize_date_string(date_line, ref)
        try:
            return datetime.strptime(date_str, '%d %B %Y')
        except ValueError:
            raise DataNotFoundException(data=self.service, ref=ref)

    def _normalize_date_string(self, date_line, ref):
        date_line_clean = " ".join(date_line.split()).lower()
        date_line_clean = date_line_clean.replace('1er', '1').replace('du', '')

        date_part = re.search(self.DATE_PATTERN, date_line_clean)
        if not date_part:
            raise DataNotFoundException(data=self.service, ref=ref)

        date_str = date_part.group(1)
        return re.sub(self.DATE_EXTRACT_PATTERN, lambda m: f"{m.group(1)} {m.group(2)} {m.group(3)}", date_str)
