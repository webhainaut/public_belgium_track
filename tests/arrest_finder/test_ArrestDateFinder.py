from main.arrest_finder.arrestDateFinder import ArrestDateFinder
from tests.arrest_finder.testAbstract_Finder import TestAbstractFinder


class TestArrestDateFinder(TestAbstractFinder):

    def setUp(self):
        self.arrestDateFinder = ArrestDateFinder("finder")

    def test_find_date_simple_format(self):
        arrest_ref = "255267"
        reader = self.read_pdf(arrest_ref)
        find_date, error = self.arrestDateFinder.find(arrest_ref, reader,
                                                      {self.arrestDateFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("14/12/2022", find_date.strftime("%d/%m/%Y"), "Simple format date")

    def test_find_date_multi_space(self):
        arrest_ref = "255470"
        reader = self.read_pdf(arrest_ref)
        find_date, error = self.arrestDateFinder.find(arrest_ref, reader,
                                                      {self.arrestDateFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("12/01/2023", find_date.strftime("%d/%m/%Y"), "more space")

    def test_find_date_1er(self):
        arrest_ref = "255668"
        reader = self.read_pdf(arrest_ref)
        find_date, error = self.arrestDateFinder.find(arrest_ref, reader,
                                                      {self.arrestDateFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("01/02/2023", find_date.strftime("%d/%m/%Y"), "1er du mois -> 1 du mois")

    def test_find_date_no_on_multi_line(self):
        arrest_ref = "255844"
        reader = self.read_pdf(arrest_ref)
        find_date, error = self.arrestDateFinder.find(arrest_ref, reader,
                                                      {self.arrestDateFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("16/02/2023", find_date.strftime("%d/%m/%Y"), "n o is strange...")

    def test_find_date_29_NBSP_char(self):
        arrest_ref = "257478"
        reader = self.read_pdf(arrest_ref)
        find_date, error = self.arrestDateFinder.find(arrest_ref, reader,
                                                      {self.arrestDateFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("29/09/2023", find_date.strftime("%d/%m/%Y"), "some strange char")

    def test_find_date_other_space_char(self):
        arrest_ref = "247478"
        reader = self.read_pdf(arrest_ref)
        find_date, error = self.arrestDateFinder.find(arrest_ref, reader,
                                                      {self.arrestDateFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("30/04/2020", find_date.strftime("%d/%m/%Y"), "Some strange space")

    def test_find_date_before_is_rectified(self):
        arrest_ref = "256672"
        reader = self.read_pdf(arrest_ref)
        find_date, error = self.arrestDateFinder.find(arrest_ref, reader,
                                                      {self.arrestDateFinder.IS_RECTIFIED_LABEL: False})

        self.assertIsNone(find_date)
        self.assertEqual("finder non trouvée", error)

    def test_find_date_is_rectified(self):
        arrest_ref = "256672"
        reader = self.read_pdf(arrest_ref)
        find_date, error = self.arrestDateFinder.find(arrest_ref, reader,
                                                      {self.arrestDateFinder.IS_RECTIFIED_LABEL: True})
        self.assertEqual("02/06/2023", find_date.strftime("%d/%m/%Y"), "Some strange space")

    def test_find_date_other_lang(self):
        arrest_ref = "258357"
        reader = self.read_pdf(arrest_ref)
        find_date, error = self.arrestDateFinder.find(arrest_ref, reader,
                                                      {self.arrestDateFinder.IS_RECTIFIED_LABEL: True})
        self.assertIsNone(find_date)
        self.assertEqual("finder non trouvée", error)

    def test_find_date_no_space(self):
        arrest_ref = "258763"
        reader = self.read_pdf(arrest_ref)
        find_date, error = self.arrestDateFinder.find(arrest_ref, reader,
                                                      {self.arrestDateFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("09/02/2024", find_date.strftime("%d/%m/%Y"), "No space")

    def test_find_date_space_in_number_role(self):
        arrest_ref = "258950"
        reader = self.read_pdf(arrest_ref)
        find_date, error = self.arrestDateFinder.find(arrest_ref, reader,
                                                      {self.arrestDateFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("28/02/2024", find_date.strftime("%d/%m/%Y"), "space in number role")
