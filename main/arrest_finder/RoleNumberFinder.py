import re

from main.Exceptions.DataNotFoundException import DataNotFoundException
from main.arrest_finder.FinderAbstract import FinderAbstract
from main.arrest_finder.FinderService import FinderService


class RoleNumberFinder(FinderAbstract, FinderService):

    def _check_args_contains(self, args):
        self.args_contain_is_rectified(args)

    def _find_data(self, ref, reader, args=None):
        index_page = self._get_first_page(args)
        try:
            text = reader.pages[index_page].extract_text()
            search_first_part = re.search(self.FIRST_TITLE_PATTERN, text, re.IGNORECASE)
            if search_first_part is not None:
                text = text[:search_first_part.span()[0]]
            roles_numbers_fiter = re.findall(r'(\d+ *\d*\.\d+ *\d*\s*/\s*\w+\s*-\s*\d+)', text)
            roles_numbers = [re.findall(r'(\d+ *\d*\.\d+ *\d*)', role)[0].replace(" ", "") for role in
                             roles_numbers_fiter]
        except IndexError:
            raise DataNotFoundException(data=self.service, ref=ref)
        return roles_numbers
