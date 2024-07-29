from main.arrest_finder.AskProcessFinder import AskProcessFinder, Process
from tests.arrest_finder.testAbstract_Finder import TestAbstractFinder


class TestAskProcessFinder(TestAbstractFinder):

    def setUp(self):
        self.askProcessFinder = AskProcessFinder("finder")

    def test_find_process_annulation(self):
        arrest_ref = "247478"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Process.ANNULATION], ask_procedures, "")

    def test_find_process_strange_annulation(self):
        arrest_ref = "255267"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Process.SUSPENSION, Process.ANNULATION], ask_procedures, "")

    def test_find_process_2_process(self):
        arrest_ref = "255470"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Process.SUSPENSION, Process.ANNULATION], ask_procedures, "")

    def test_find_process_suspension(self):
        arrest_ref = "255668"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Process.SUSPENSION], ask_procedures, "")

    def test_find_process_suspension_solicite(self):
        arrest_ref = "255844"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Process.SUSPENSION], ask_procedures, "")

    def test_find_process_is_rectified(self):
        arrest_ref = "256672"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: True})
        self.assertEqual([Process.SUSPENSION], ask_procedures, "")

    def test_find_process_first_delimiter_on_second_page(self):
        arrest_ref = "255472"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Process.SUSPENSION, Process.ANNULATION], ask_procedures, "")

    def test_find_process_strange_space(self):
        arrest_ref = "255962"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Process.ANNULATION, Process.REPARATION], ask_procedures, "")

    def test_find_process(self):
        arrest_ref = "255964"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Process.ANNULATION, Process.REPARATION], ask_procedures, "")

    def test_find_process_suspension_space(self):
        arrest_ref = "255679"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Process.SUSPENSION], ask_procedures, "")

    def test_find_process_sus(self):
        arrest_ref = "256014"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Process.SUSPENSION, Process.ANNULATION], ask_procedures, "")

    def test_find_process_suspension_only(self):
        arrest_ref = "255438"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Process.SUSPENSION], ask_procedures, "")

    def test_find_process_reparation_only(self):
        arrest_ref = "255681"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Process.REPARATION], ask_procedures, "")

    def test_find_process_suspension_poursuite(self):
        arrest_ref = "256484"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Process.SUSPENSION], ask_procedures, "")

    def test_find_process_annulation_2(self):
        arrest_ref = "257654"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Process.ANNULATION], ask_procedures, "")

    def test_find_process_requete_suspension_annulation(self):
        arrest_ref = "257919"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Process.SUSPENSION, Process.ANNULATION], ask_procedures, "")

    def test_find_process_recours_suspension(self):
        arrest_ref = "257921"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Process.SUSPENSION], ask_procedures, "")

    def test_find_process_suspension_2(self):
        arrest_ref = "255678"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Process.SUSPENSION], ask_procedures, "")

    def test_find_process_annulation_3(self):
        arrest_ref = "257819"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Process.ANNULATION], ask_procedures, "")

    def test_find_process_reparation(self):
        arrest_ref = "258245"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Process.REPARATION], ask_procedures, "")

    def test_find_process_annulation_in_procedure(self):
        arrest_ref = "256675"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Process.SUSPENSION, Process.ANNULATION], ask_procedures, "")

    def test_find_process_reparation_2(self):
        arrest_ref = "257009"
        reader = self.read_pdf(arrest_ref)
        ask_procedures = self.askProcessFinder.find(arrest_ref, reader,
                                                    {self.askProcessFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Process.ANNULATION, Process.REPARATION], ask_procedures, "")
