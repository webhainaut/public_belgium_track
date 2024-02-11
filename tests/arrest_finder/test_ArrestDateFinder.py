from main.Exceptions.DataNotFoundException import DataNotFoundException
from main.arrest_finder.ArrestDateFinder import ArrestDateFinder
from tests.arrest_finder.test_FinderAbstract import TestFinderAbstract


class TestArrestDateFinder(TestFinderAbstract):

    def setUp(self):
        self.arrestDateFinder = ArrestDateFinder("finder")

    def test_kwargs_contain_arg_no_dic(self):
        with self.assertRaises(NotADirectoryError) as context:
            self.arrestDateFinder.kwargs_contain_arg(None)
        self.assertEqual("isRectified no in the dic", str(context.exception))

    def test_kwargs_contain_arg_bad_dic(self):
        with self.assertRaises(NotADirectoryError) as context:
            self.arrestDateFinder.kwargs_contain_arg({"coucou": 1})
        self.assertEqual("isRectified no in the dic", str(context.exception))

    def test_kwargs_contain_arg_ok(self):
        self.arrestDateFinder.kwargs_contain_arg({self.arrestDateFinder.IS_RECTIFIED_LABEL: True})

    def test_find_date_simple_format(self):
        arrest_ref = "255267"
        reader = self.read_pdf(arrest_ref)
        find_date = self.arrestDateFinder.find(arrest_ref, reader, {self.arrestDateFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("14/12/2022", find_date.strftime("%d/%m/%Y"), "Simple format date")

    def test_find_date_multi_space(self):
        arrest_ref = "255470"
        reader = self.read_pdf(arrest_ref)
        find_date = self.arrestDateFinder.find(arrest_ref, reader, {self.arrestDateFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("12/01/2023", find_date.strftime("%d/%m/%Y"), "more space")

    def test_find_date_1er(self):
        arrest_ref = "255668"
        reader = self.read_pdf(arrest_ref)
        find_date = self.arrestDateFinder.find(arrest_ref, reader, {self.arrestDateFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("01/02/2023", find_date.strftime("%d/%m/%Y"), "1er du mois -> 1 du mois")

    def test_find_date_no_on_multi_line(self):
        arrest_ref = "255844"
        reader = self.read_pdf(arrest_ref)
        find_date = self.arrestDateFinder.find(arrest_ref, reader, {self.arrestDateFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("16/02/2023", find_date.strftime("%d/%m/%Y"), "n o is strange...")

    def test_find_date_29_NBSP_char(self):
        arrest_ref = "257478"
        reader = self.read_pdf(arrest_ref)
        find_date = self.arrestDateFinder.find(arrest_ref, reader, {self.arrestDateFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("29/09/2023", find_date.strftime("%d/%m/%Y"), "some strange char")

    def test_find_date_other_space_char(self):
        arrest_ref = "247478"
        reader = self.read_pdf(arrest_ref)
        find_date = self.arrestDateFinder.find(arrest_ref, reader, {self.arrestDateFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("30/04/2020", find_date.strftime("%d/%m/%Y"), "Some strange space")

    def test_find_date_before_is_rectified(self):
        arrest_ref = "256672"
        reader = self.read_pdf(arrest_ref)
        with self.assertRaises(DataNotFoundException) as context:
            self.arrestDateFinder.find(arrest_ref, reader, {self.arrestDateFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("finder non trouvée dans le pdf 256672 ", str(context.exception))

    def test_find_date_is_rectified(self):
        arrest_ref = "256672"
        reader = self.read_pdf(arrest_ref)
        find_date = self.arrestDateFinder.find(arrest_ref, reader, {self.arrestDateFinder.IS_RECTIFIED_LABEL: True})
        self.assertEqual("02/06/2023", find_date.strftime("%d/%m/%Y"), "Some strange space")
