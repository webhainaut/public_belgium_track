import re

from main.arrest_finder.FinderAbstract import FinderAbstract


class IsRectifiedFinder(FinderAbstract):

    def __find_data(self, ref, reader, args=None):
        return re.search(r'(arrêt n.* du .* est rectif.* par .*arrêt n.* du .*)',
                         reader.pages[0].extract_text()) is not None
