from pypdf import PdfReader

from main.arrest_finder.finderAbstract import FinderAbstract
from main.arrest_finder.finderService import FinderService


class KeywordsFinder(FinderAbstract, FinderService):
    KEYWORDS = "KEYWORDS"

    def _check_args_contains(self, args):
        if args is None or self.KEYWORDS not in args:
            raise NotADirectoryError("{KEYWORDS} no in the dic".format(KEYWORDS=self.KEYWORDS))
        if args[self.KEYWORDS] is None or not isinstance(args[self.KEYWORDS], list):
            raise NotADirectoryError("KEYWORDS need a list")

    def _find_data(self, ref, reader: PdfReader, args=None):
        keywords = args[self.KEYWORDS]
        keywords_find = []
        for keyword in keywords:
            if self.search_word(self.service, ref, reader, keyword):
                keywords_find.append(keyword)
        return keywords_find
