import locale
import unittest
from datetime import datetime
from unittest import TestCase

from pypdf import PdfReader

from Arrest import Arrest, Process
from Exceptions.DataNotFoundException import DataNotFoundException

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

    def test_find_date_multi_space(self):
        arrest_ref = "255470"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_arrest_date()
        self.assertEqual("12/01/2023", arrest.arrest_date.strftime("%d/%m/%Y"), "more space")

    def test_find_date_1er(self):
        arrest_ref = "255668"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_arrest_date()
        self.assertEqual("01/02/2023", arrest.arrest_date.strftime("%d/%m/%Y"), "1er du mois -> 1 du mois")

    def test_find_date_no_on_multi_line(self):
        arrest_ref = "255844"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_arrest_date()
        self.assertEqual("16/02/2023", arrest.arrest_date.strftime("%d/%m/%Y"), "n o is strange...")

    def test_find_date_29_NBSP_char(self):
        arrest_ref = "257478"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_arrest_date()
        self.assertEqual("29/09/2023", arrest.arrest_date.strftime("%d/%m/%Y"), "some strange char")

    def test_find_date_other_space_char(self):
        arrest_ref = "247478"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_arrest_date()
        self.assertEqual("30/04/2020", arrest.arrest_date.strftime("%d/%m/%Y"), "Some strange space")

    def test_find_date_before_is_rectified(self):
        arrest_ref = "256672"
        arrest = self.read_pdf(arrest_ref)
        with self.assertRaises(DataNotFoundException) as context:
            arrest.find_arrest_date()
        self.assertEqual("Date de l'arrêt non trouvée dans le pdf 256672 ", str(context.exception))

    def test_is_rectified_not_found(self):
        arrest_ref = "247478"
        arrest = self.read_pdf(arrest_ref)
        arrest.is_rectified()
        self.assertFalse(arrest.rectified)

    def test_is_rectified_found(self):
        arrest_ref = "256672"
        arrest = self.read_pdf(arrest_ref)
        arrest.is_rectified()
        self.assertTrue(arrest.rectified)

    def test_from_dic(self):
        arrest_ref = "256672"
        arrest = Arrest(arrest_ref, None, datetime.strptime("23/06/2023", '%d/%m/%Y'), "ceci")
        arrest.rectified = True
        arrest.arrest_date = datetime(2022, 5, 23)
        arrest.procedures = [Process.ANNULATION, Process.SUSPENSION]
        arrest_from_dic = Arrest.from_dic(arrest.as_dict())
        self.assertEqual(arrest.as_dict(), arrest_from_dic.as_dict())

    def test_find_process_annulation(self):
        arrest_ref = "247478"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_process()
        self.assertEqual([Process.ANNULATION], arrest.procedures, "")

    def test_find_process_strange_annulation(self):
        arrest_ref = "255267"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_process()
        self.assertEqual([Process.SUSPENSION, Process.ANNULATION], arrest.procedures, "")

    def test_find_process_2_process(self):
        arrest_ref = "255470"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_process()
        self.assertEqual([Process.SUSPENSION, Process.ANNULATION], arrest.procedures, "")

    def test_find_process_suspension(self):
        arrest_ref = "255668"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_process()
        self.assertEqual([Process.SUSPENSION], arrest.procedures, "")

    def test_find_process_suspension_solicite(self):
        arrest_ref = "255844"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_process()
        self.assertEqual([Process.SUSPENSION], arrest.procedures, "")

    def test_find_process_is_rectified(self):
        arrest_ref = "256672"
        arrest = self.read_pdf(arrest_ref)
        arrest.is_rectified().find_process()
        self.assertEqual([Process.SUSPENSION], arrest.procedures, "")

    def test_find_process_first_delimiter_on_second_page(self):
        arrest_ref = "255472"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_process()
        self.assertEqual([Process.SUSPENSION, Process.ANNULATION], arrest.procedures, "")

    def test_find_process_strange_space(self):
        arrest_ref = "255962"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_process()
        self.assertEqual([Process.ANNULATION, Process.REPARATION], arrest.procedures, "")

    def test_find_process(self):
        arrest_ref = "255964"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_process()
        self.assertEqual([Process.ANNULATION, Process.REPARATION], arrest.procedures, "")

    def test_find_process_suspension_space(self):
        arrest_ref = "255679"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_process()
        self.assertEqual([Process.SUSPENSION], arrest.procedures, "")

    def test_find_process_sus(self):
        arrest_ref = "256014"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_process()
        self.assertEqual([Process.SUSPENSION, Process.ANNULATION], arrest.procedures, "")

    def test_find_process_suspension_only(self):
        arrest_ref = "255438"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_process()
        self.assertEqual([Process.SUSPENSION], arrest.procedures, "")

    def test_find_process_reparation_only(self):
        arrest_ref = "255681"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_process()
        self.assertEqual([Process.REPARATION], arrest.procedures, "")

    def test_find_process_suspension_poursuite(self):
        arrest_ref = "256484"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_process()
        self.assertEqual([Process.SUSPENSION], arrest.procedures, "")

    def test_find_process_annulation_2(self):
        arrest_ref = "257654"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_process()
        self.assertEqual([Process.ANNULATION], arrest.procedures, "")

    def test_find_process_requete_suspension_annulation(self):
        arrest_ref = "257919"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_process()
        self.assertEqual([Process.SUSPENSION, Process.ANNULATION], arrest.procedures, "")

    def test_find_process_recours_suspension(self):
        arrest_ref = "257921"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_process()
        self.assertEqual([Process.SUSPENSION], arrest.procedures, "")

    def test_find_process_suspension_2(self):
        arrest_ref = "255678"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_process()
        self.assertEqual([Process.SUSPENSION], arrest.procedures, "")

    def test_find_process_annulation_3(self):
        arrest_ref = "257819"
        arrest = self.read_pdf(arrest_ref)
        arrest.find_process()
        self.assertEqual([Process.ANNULATION], arrest.procedures, "")


if __name__ == '__main__':
    unittest.main()
