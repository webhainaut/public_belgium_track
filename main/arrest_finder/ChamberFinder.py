import re

from main.Exceptions.DataNotFoundException import DataNotFoundException
from main.arrest_finder.FinderAbstract import FinderAbstract
from main.arrest_finder.FinderService import FinderService


class ChamberFinder(FinderAbstract, FinderService):
    """ Trouve la chambre du conseil qui a traité l'arrêt """

    def _check_args_contains(self, args):
        self.args_contain_is_rectified(args)

    def _find_data(self, ref, reader, args=None):
        index_page = self._get_first_page(args)
        second_delimiter_pattern = r'([A|À]\s*R\s*R\s*[Ê|Ë|E]\s*T|S\s*I\s*É\s*G\s*E\s*A\s*N\s*T)'
        text = self.extract_text_between_delimiters_for_reader(self.service, ref, reader,
                                                               pattern_delimiter_2=second_delimiter_pattern,
                                                               page_1=index_page, page_2=index_page + 1,
                                                               flags=re.DOTALL)
        try:
            chamber = self.search_chamber(text)
        except IndexError:
            raise DataNotFoundException(data=self.service, ref=ref)
        return chamber

    @staticmethod
    def search_chamber(text):
        chamber = re.findall(r'\w+e', text)
        return chamber[-1][:-1]
