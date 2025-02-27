import re

from main.Exceptions.DataNotFoundException import DataNotFoundException
from main.Models.Models import CaseModel
from main.arrest_finder.FinderAbstract import FinderAbstract
from main.arrest_finder.FinderService import FinderService
from main.dao.arrest_dao import ArrestDao
from main.dao.case_dao import CaseDao


class CasesFinder(FinderAbstract, FinderService):

    def __init__(self, service):
        super().__init__(service)
        self.arrest_dao = ArrestDao()
        self.case_dao = CaseDao()

    def _check_args_contains(self, args):
        self.args_contain_is_rectified(args)

    def _find_data(self, ref, reader, args=None):
        index_page = self._get_first_page(args)
        second_delimiter_pattern = self.FIRST_TITLE_PATTERN
        text = self.extract_text_between_delimiters_for_reader(self.service, ref, reader,
                                                               pattern_delimiter_2=second_delimiter_pattern,
                                                               page_1=index_page, page_2=index_page + 1)
        try:
            roles_numbers_fiter = re.findall(r'\d+ *\d*\.\d+ *\d*\s*/\s*\w+\s*\w*-\s*\d+', text)
            roles_numbers = [re.findall(r'(\d+ *\d*\.\d+ *\d*)', role)[0].replace(" ", "") for role in
                             roles_numbers_fiter]
        except IndexError:
            raise DataNotFoundException(data=self.service, ref=ref)
        return self._get_cases(roles_numbers)

    def _get_cases(self, roles_numbers):
        cases = []
        for roles_number in roles_numbers:
            case = self.case_dao.get(roles_number)
            if case is None:
                cases.append(CaseModel(numRole=roles_number))
            else:
                cases.append(case)
        return cases
