from main.arrest_finder.casesFinder import CasesFinder
from tests.arrest_finder.testAbstract_Finder import TestAbstractFinder


class TestCasesFinder(TestAbstractFinder):

    def setUp(self):
        self.casesFinder = CasesFinder("finder")

    def test_find_role_only_one(self):
        arrest_ref = "247478"
        reader = self.read_pdf(arrest_ref)
        cases, error = self.casesFinder.find(arrest_ref, reader,
                                             {self.casesFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual("205.687", cases[0].numRole, "Only one")

    def test_find_role_several(self):
        arrest_ref = "255472"
        reader = self.read_pdf(arrest_ref)
        cases, error = self.casesFinder.find(arrest_ref, reader,
                                             {self.casesFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(
            ["236.088", "236.089", "236.090", "236.091", "236.092", "236.093", "236.094",
             "236.095", "236.098", "236.099", "236.100", "236.101", "236.103", "236.105",
             "236.122", "236.124", "236.126", "236.127", "236.128", "236.130", "236.131",
             "236.133", "236.134", "236.135", "236.137", "236.138", "236.143", "236.144",
             "236.145", "236.146", "236.147", "236.148", "236.151", "236.156"], [case.numRole for case in cases],
            "Only one")

    def test_find_role_is_rectified(self):
        arrest_ref = "256672"
        reader = self.read_pdf(arrest_ref)
        cases, error = self.casesFinder.find(arrest_ref, reader,
                                             {self.casesFinder.IS_RECTIFIED_LABEL: True})
        self.assertEqual(["238.917"], [case.numRole for case in cases], "Only one rectified")

    def test_find_role_no_space(self):
        arrest_ref = "255824"
        reader = self.read_pdf(arrest_ref)
        cases, error = self.casesFinder.find(arrest_ref, reader,
                                             {self.casesFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(["233.277"], [case.numRole for case in cases], "No space after the A.")

    def test_find_role_no_A(self):
        arrest_ref = "240250"
        reader = self.read_pdf(arrest_ref)
        cases, error = self.casesFinder.find(arrest_ref, reader,
                                             {self.casesFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(["208.478"], [case.numRole for case in cases], "No  A.")

    def test_find_role_space(self):
        arrest_ref = "258274"
        reader = self.read_pdf(arrest_ref)
        cases, error = self.casesFinder.find(arrest_ref, reader,
                                             {self.casesFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(["240.318"], [case.numRole for case in cases], "")

    def test_find_role_no_2(self):
        arrest_ref = "255681"
        reader = self.read_pdf(arrest_ref)
        cases, error = self.casesFinder.find(arrest_ref, reader,
                                             {self.casesFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(["233.648"], [case.numRole for case in cases], "")

    def test_find_role_no_3(self):
        arrest_ref = "259294"
        reader = self.read_pdf(arrest_ref)
        cases, error = self.casesFinder.find(arrest_ref, reader,
                                             {self.casesFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(["241.407"], [case.numRole for case in cases], "")

    def test_find_role_a(self):
        arrest_ref = "260008"
        reader = self.read_pdf(arrest_ref)
        cases, error = self.casesFinder.find(arrest_ref, reader,
                                             {self.casesFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(["241.769"], [case.numRole for case in cases], "")
