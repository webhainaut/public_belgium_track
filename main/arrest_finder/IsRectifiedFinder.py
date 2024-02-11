import re

from main.arrest_finder.FinderInterface import FinderInterface


class IsRectifiedFinder(FinderInterface):

    def find(self, ref, reader, args=None):
        return re.search(r'(arrêt n.* du .* est rectif.* par .*arrêt n.* du .*)',
                         reader.pages[0].extract_text()) is not None
