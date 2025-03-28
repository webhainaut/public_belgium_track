import re

from main.arrest_finder.finderAbstract import FinderAbstract


class IsRectifiedFinder(FinderAbstract):

    def _check_args_contains(self, args):
        pass

    def _find_data(self, ref, reader, args=None):
        return re.search(r'(arrêt n.* du .* est rectif.* par .*arrêt n.* du .*)',
                         reader.pages[0].extract_text()) is not None
