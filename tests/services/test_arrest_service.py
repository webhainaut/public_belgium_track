import locale
import os
import unittest
from typing import List
from unittest import TestCase

from pypdf import PdfReader

from main.Models.Models import ArrestModel, RulingModel, CaseModel, KeywordModel
from main.arrest_finder.RulingsFinder import Ruling
from main.services.arrest_service import ArrestService

locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')


class TestArrestService(TestCase):

    @staticmethod
    def read_pdf(ref):
        root_path = os.path.abspath(os.path.dirname(__file__)) + "/../"
        return PdfReader(root_path + "resources/arrests/{ref}.pdf".format(ref=ref))

    def setUp(self):
        self.arrest_service = ArrestService()

    def test_is_rectified(self):
        ref = "256672"
        reader = self.read_pdf(ref)
        arrest = ArrestModel(ref=ref)
        is_rectified = self.arrest_service.is_rectified(ref, reader, arrest)
        self.assertTrue(is_rectified)

    def test_find_arrest_date(self):
        ref = "255267"
        reader = self.read_pdf(ref)
        arrest = ArrestModel(ref=ref, is_rectified = False)
        arrest_date = self.arrest_service.find_arrest_date(ref, reader, arrest)
        self.assertEqual("14/12/2022", arrest_date.strftime("%d/%m/%Y"))

    def test_find_rulings_with_surlpus(self):
        ref = "258204"
        reader = self.read_pdf(ref)
        arrest = ArrestModel(ref=ref, is_rectified = False)
        rulings : List[RulingModel] = self.arrest_service.find_rulings(ref, reader, arrest)
        self.assertEqual(Ruling.ORDERED, rulings[0].ruling)
        self.assertTrue(rulings[0].surplus)

    def test_find_rulings_without_surplus(self):
        ref = "256835"
        reader = self.read_pdf(ref)
        arrest = ArrestModel(ref=ref, is_rectified = False)
        rulings : List[RulingModel] = self.arrest_service.find_rulings(ref, reader, arrest)
        self.assertEqual(2, len(rulings))
        self.assertEqual(Ruling.ISSUES_DECREE, rulings[0].ruling)
        self.assertEqual(Ruling.NO_LONGER_REQUIRED, rulings[1].ruling)

    def test_find_cases(self):
        ref = "255472"
        reader = self.read_pdf(ref)
        arrest = ArrestModel(ref=ref, is_rectified = False)
        cases : List[CaseModel] = self.arrest_service.find_cases(ref, reader, arrest)
        self.assertEqual(34, len(cases))

    def test_find_keywords(self):
        ref = "247478"
        reader = self.read_pdf(ref)
        arrest = ArrestModel(ref=ref, is_rectified = False)
        title = "title"
        keyword_1 = "interventions"
        keywords : List[KeywordModel] = self.arrest_service.find_keywords(title, ["test", keyword_1], ref, reader, arrest)
        self.assertEqual(title, keywords[0].title)
        self.assertEqual(keyword_1, keywords[0].word)



if __name__ == '__main__':
    unittest.main()
