import locale
from unittest import TestCase

from pypdf import PdfReader

from Arrest import Arrest

locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')


class TestArrest(TestCase):
    def test_find_date_simple_format(self):
        arrest_ref = 255267
        arrest = self.read_pdf(arrest_ref)
        arrest.find_date()
        self.assertEqual("14/12/2022", arrest.date.strftime("%d/%m/%Y"), "Simple format date")

    def test_find_date_multi_space(self):
        arrest_ref = 255470
        arrest = self.read_pdf(arrest_ref)
        arrest.find_date()
        self.assertEqual("12/01/2023", arrest.date.strftime("%d/%m/%Y"), "more space")

    def test_find_date_1er(self):
        arrest_ref = 255668
        arrest = self.read_pdf(arrest_ref)
        arrest.find_date()
        self.assertEqual("01/02/2023", arrest.date.strftime("%d/%m/%Y"), "1er du mois -> 1 du mois")

    def test_find_date_no_on_multi_line(self):
        arrest_ref = 255844
        arrest = self.read_pdf(arrest_ref)
        arrest.find_date()
        self.assertEqual("16/02/2023", arrest.date.strftime("%d/%m/%Y"), "n o is strange...")

    def test_find_date_29_NBSP_char(self):
        arrest_ref = 257478
        arrest = self.read_pdf(arrest_ref)
        arrest.find_date()
        self.assertEqual("29/09/2023", arrest.date.strftime("%d/%m/%Y"), "some strange char")

    def test_find_date_other_space_char(self):
        arrest_ref = 247478
        arrest = self.read_pdf(arrest_ref)
        arrest.find_date()
        self.assertEqual("30/04/2020", arrest.date.strftime("%d/%m/%Y"), "Some strange space")

    def test_find_date_before_is_rectified(self):
        arrest_ref = 256672
        arrest = self.read_pdf(arrest_ref)
        self.assertRaises(IndexError, arrest.find_date)

    @staticmethod
    def read_pdf(arrest_ref):
        reader = PdfReader("./resources/arrests/{ref}.pdf".format(ref=arrest_ref))
        arrest = Arrest(arrest_ref, reader)
        return arrest
