from main.arrest_finder.ChamberFinder import ChamberFinder
from tests.arrest_finder.testAbstract_Finder import TestAbstractFinder


class TestChamberFinder(TestAbstractFinder):

    def setUp(self):
        self.chamberFinder = ChamberFinder("finder")

    def test_find_role_only_one(self):
        arrest_ref = "247478"
        reader = self.read_pdf(arrest_ref)
        chamber, error = self.chamberFinder.find(arrest_ref, reader,
                                                 {self.chamberFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("XIII", chamber)

    def test_find_role_5bis(self):
        arrest_ref = "259294"
        reader = self.read_pdf(arrest_ref)
        chamber, error = self.chamberFinder.find(arrest_ref, reader,
                                                 {self.chamberFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("Vbis", chamber)

    def test_find_role_VI(self):
        arrest_ref = "261697"
        reader = self.read_pdf(arrest_ref)
        chamber, error = self.chamberFinder.find(arrest_ref, reader,
                                                 {self.chamberFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("VI", chamber)

    def test_find_role_e(self):
        arrest_ref = "259666"
        reader = self.read_pdf(arrest_ref)
        chamber, error = self.chamberFinder.find(arrest_ref, reader,
                                                 {self.chamberFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("VI", chamber)

    def test_find_role_re(self):
        arrest_ref = "261634"
        reader = self.read_pdf(arrest_ref)
        chamber, error = self.chamberFinder.find(arrest_ref, reader,
                                                 {self.chamberFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("VI", chamber)

    def test_find_role_siegeant(self):
        arrest_ref = "259507"
        reader = self.read_pdf(arrest_ref)
        chamber, error = self.chamberFinder.find(arrest_ref, reader,
                                                 {self.chamberFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("VI", chamber)
