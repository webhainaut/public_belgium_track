import locale
import unittest
from datetime import datetime
from unittest import TestCase

from pypdf import PdfReader

from main.Arrest import Arrest
from main.arrest_finder.AskProcessFinder import Process

locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')


class TestArrest(TestCase):
    @staticmethod
    def read_pdf(arrest_ref):
        reader = PdfReader("./resources/arrests/{ref}.pdf".format(ref=arrest_ref))
        arrest = Arrest(arrest_ref, reader, datetime.strptime("14/12/2022", '%d/%m/%Y'), "public")
        return arrest

    def test_find_date_simple_format(self):
        arrest_ref = "255267"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_arrest_date()
        self.assertEqual("14/12/2022", arrest.arrest_date.strftime("%d/%m/%Y"), "Simple format date")

    def test_is_rectified_not_found(self):
        arrest_ref = "247478"
        arrest = self.read_pdf(arrest_ref)
        arrest.is_rectified()
        self.assertFalse(arrest.isRectified)

    def test_is_rectified_found(self):
        arrest_ref = "256672"
        arrest = self.read_pdf(arrest_ref)
        arrest.is_rectified()
        self.assertTrue(arrest.isRectified)

    def test_from_dic(self):
        arrest_ref = "256672"
        arrest = Arrest(arrest_ref, None, datetime.strptime("23/06/2023", '%d/%m/%Y'), "ceci")
        arrest.isRectified = True
        arrest.arrest_date = datetime(2022, 5, 23)
        arrest.ask_procedures = [Process.ANNULATION, Process.SUSPENSION]
        arrest_from_dic = Arrest.from_dic(arrest.as_dict())
        self.assertEqual(arrest.ref, arrest_from_dic.ref)
        self.assertEqual(arrest.publish_date, arrest_from_dic.publish_date)
        self.assertEqual(arrest.contract_type, arrest_from_dic.contract_type)


def test_find_process_annulation(self):
    arrest_ref = "247478"
    arrest = self.read_pdf(arrest_ref)
    arrest.find_ask_process()
    self.assertEqual([Process.ANNULATION], arrest.ask_procedures, "")


if __name__ == '__main__':
    unittest.main()
