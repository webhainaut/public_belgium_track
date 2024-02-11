import re
from datetime import datetime

from main.Exceptions.DataNotFoundException import DataNotFoundException
from main.arrest_finder.FinderInterface import FinderInterface


class ArrestDateFinder(FinderInterface):
    """find the date of arrest
    Attention quand plusieurs espace
    des fois, 1er ...
    parfois n\n o
    """

    def find(self, ref, reader, args=None):
        self.kwargs_contain_arg(args)
        index_page = 0 if not args[self.IS_RECTIFIED_LABEL] else 1
        try:
            date_line = re.findall(r'(n\s*o\s.*\sdu\s\d{1,2}.*\s\d{4})', reader.pages[index_page].extract_text())[
                0]
        except IndexError:
            raise DataNotFoundException(data=self.label, ref=ref)
        date_line_clean = " ".join(date_line.split()).replace('1er', '1')
        return datetime.strptime(re.findall(r'(\d{1,2} \w* \d{4}$)', date_line_clean)[0], '%d %B %Y')

    def kwargs_contain_arg(self, kwargs):
        if kwargs is None or self.IS_RECTIFIED_LABEL not in kwargs:
            raise NotADirectoryError("{rectified} no in the dic".format(rectified=self.IS_RECTIFIED_LABEL))
