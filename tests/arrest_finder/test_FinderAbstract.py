import locale
import os
from unittest import TestCase

from pypdf import PdfReader

locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')


class TestFinderAbstract(TestCase):

    @staticmethod
    def read_pdf(arrest_ref):
        return PdfReader(
            os.path.abspath(os.path.dirname(__file__)) + "/../resources/arrests/{ref}.pdf".format(ref=arrest_ref))
