from unittest import TestCase

from main.arrest_finder.FinderAbstract import FinderAbstract


class TestFinderAbstract(TestCase):

    def setUp(self):
        self.finder = FinderAbstract("finder")

    def test_kwargs_contain_arg_no_dic(self):
        with self.assertRaises(NotADirectoryError) as context:
            self.finder.kwargs_contain_is_rectified(None)
        self.assertEqual("isRectified no in the dic", str(context.exception))

    def test_kwargs_contain_arg_bad_dic(self):
        with self.assertRaises(NotADirectoryError) as context:
            self.finder.kwargs_contain_is_rectified({"coucou": 1})
        self.assertEqual("isRectified no in the dic", str(context.exception))

    def test_kwargs_contain_arg_ok(self):
        self.finder.kwargs_contain_is_rectified({self.finder.IS_RECTIFIED_LABEL: True})

    def test_get_first_age_1(self):
        self.assertEqual(1, self.finder.get_first_page({self.finder.IS_RECTIFIED_LABEL: True}))

    def test_get_first_age_0(self):
        self.assertEqual(0, self.finder.get_first_page({self.finder.IS_RECTIFIED_LABEL: False}))
