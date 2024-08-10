from main.arrest_finder.KeywordsFinder import KeywordsFinder
from tests.arrest_finder.testAbstract_Finder import TestAbstractFinder


class TestKeywordsFinder(TestAbstractFinder):
    def setUp(self):
        self.keywordsFinder = KeywordsFinder("finder")

    def test_find_keywords(self):
        arrest_ref = "247478"
        reader = self.read_pdf(arrest_ref)
        search1 = "annulation"
        search2 = "Orp-le"
        search3 = "Orp-le-petit"
        search4 = "vern"
        search5 = "annulations"
        words, error = self.keywordsFinder.find(arrest_ref, reader,
                                                {self.keywordsFinder.KEYWORDS: [search1, search2, search3, search4,
                                                                                search5]})
        self.assertEqual([search1, search2], words, "")
