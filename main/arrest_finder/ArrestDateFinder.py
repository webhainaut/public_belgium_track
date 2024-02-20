import re
from datetime import datetime

from main.Exceptions.DataNotFoundException import DataNotFoundException
from main.arrest_finder.FinderAbstract import FinderAbstract
from main.arrest_finder.FinderService import FinderService


class ArrestDateFinder(FinderAbstract, FinderService):
    """find the date of arrest
    Attention quand plusieurs espace
    des fois, 1er ...
    parfois n\n o
    """

    def _check_args_contains(self, args):
        self.args_contain_is_rectified(args)

    def _find_data(self, ref, reader, args=None):
        index_page = self._get_first_page(args)
        try:
            date_line = re.findall(r'(n\s*o\s.*\sdu\s\d{1,2}.*\s\d{4})', reader.pages[index_page].extract_text())[
                0]
        except IndexError:
            raise DataNotFoundException(data=self.service, ref=ref)
        date_line_clean = " ".join(date_line.split()).replace('1er', '1')
        return datetime.strptime(re.findall(r'(\d{1,2} \w* \d{4}$)', date_line_clean)[0], '%d %B %Y')
