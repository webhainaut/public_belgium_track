from main.arrest_finder.RulingsFinder import RulingsFinder, Ruling
from tests.arrest_finder.testAbstract_Finder import TestAbstractFinder


class TestRulingsFinder(TestAbstractFinder):
    def setUp(self):
        self.rulingsFinder = RulingsFinder("finder")

    def test_find_rulings_issues_decree(self):
        arrest_ref = "247478"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(Ruling.ISSUES_DECREE.label, rulings[0].ruling, "")
        self.assertFalse(rulings[0].surplus)

    def test_find_rulings_ordonne(self):
        arrest_ref = "255267"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(Ruling.ORDERED.label, rulings[0].ruling, "")
        self.assertFalse(rulings[0].surplus)

    def test_find_rulings_is_rectified(self):
        arrest_ref = "256672"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: True})
        self.assertEqual([], rulings, "is rectified not check for now")

    def test_find_rulings_multi_page_title(self):
        arrest_ref = "256484"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(Ruling.REJECT.label, rulings[0].ruling, "Title Ruling juste before the next page")
        self.assertFalse(rulings[0].surplus)

    def test_find_rulings_no_required(self):
        arrest_ref = "255472"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(Ruling.NO_LONGER_REQUIRED.label, rulings[0].ruling)
        self.assertFalse(rulings[0].surplus)

    def test_find_rulings_reject(self):
        arrest_ref = "255668"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(Ruling.REJECT.label, rulings[0].ruling)
        self.assertFalse(rulings[0].surplus)

    def test_find_rulings_no_second_delimiter_found(self):
        arrest_ref = "255678"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(Ruling.NO_LONGER_REQUIRED.label, rulings[0].ruling)
        self.assertFalse(rulings[0].surplus)

    def test_find_rulings_acknowledge_decree(self):
        arrest_ref = "255681"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(Ruling.ACKNOWLEDGE_DECREE.label, rulings[0].ruling)
        self.assertFalse(rulings[0].surplus)

    def test_find_rulings_cancelled(self):
        arrest_ref = "257654"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(Ruling.CANCELLED.label, rulings[0].ruling)
        self.assertFalse(rulings[0].surplus)

    def test_find_rulings_request_reject(self):
        arrest_ref = "257819"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(Ruling.REJECT.label, rulings[0].ruling)
        self.assertFalse(rulings[0].surplus)

    def test_find_rulings_ordonne_with_surplus(self):
        arrest_ref = "258204"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Ruling.REJECT.label, Ruling.ORDERED.label], [ruling.ruling for ruling in rulings])
        self.assertTrue(rulings[0].surplus)
        self.assertFalse(rulings[1].surplus)

    def test_find_rulings_uncompleted(self):
        arrest_ref = "255568"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(Ruling.UNCOMPLETED.label, rulings[0].ruling)
        self.assertFalse(rulings[0].surplus)

    def test_find_rulings_is_ordered(self):
        arrest_ref = "258317"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Ruling.REJECT.label, Ruling.ORDERED.label], [ruling.ruling for ruling in rulings])
        self.assertTrue(isinstance(rulings[0].surplus, bool) and rulings[0].surplus)
        self.assertFalse(rulings[1].surplus)

    def test_find_rulings_sine_die(self):
        arrest_ref = "255713"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(Ruling.SINE_DIE.label, rulings[0].ruling)
        self.assertFalse(rulings[0].surplus)

    def test_find_rulings_cancelled_2(self):
        arrest_ref = "256352"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(Ruling.CANCELLED.label, rulings[0].ruling)
        self.assertFalse(rulings[0].surplus)

    def test_find_rulings_request_intervention_not_interest(self):
        arrest_ref = "256552"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(Ruling.NO_LONGER_REQUIRED.label, rulings[0].ruling)
        self.assertFalse(rulings[0].surplus)

    def test_find_rulings_2_rulings(self):
        arrest_ref = "256835"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Ruling.ISSUES_DECREE.label, Ruling.NO_LONGER_REQUIRED.label],
                         [ruling.ruling for ruling in rulings])
        self.assertFalse(rulings[0].surplus)
        self.assertFalse(rulings[1].surplus)

    def test_find_rulings_ordered_with_surplus(self):
        arrest_ref = "256952"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([ Ruling.REJECT.label, Ruling.ORDERED.label], [ruling.ruling for ruling in rulings])
        self.assertTrue(rulings[0].surplus)
        self.assertFalse(rulings[1].surplus)

    def test_find_rulings_lift(self):
        arrest_ref = "257003"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(Ruling.LIFT.label, rulings[0].ruling)
        self.assertFalse(rulings[0].surplus)

    def test_find_rulings_annulation_suspension_diff(self):
        arrest_ref = "255570"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Ruling.LIFT.label, Ruling.NO_LONGER_REQUIRED.label], [ruling.ruling for ruling in rulings])
        self.assertFalse(rulings[0].surplus)
        self.assertFalse(rulings[1].surplus)

    def test_find_rulings_lift_and_acknowledge_decree(self):
        arrest_ref = "255962"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Ruling.LIFT.label, Ruling.ACKNOWLEDGE_DECREE.label], [ruling.ruling for ruling in rulings])
        self.assertFalse(rulings[0].surplus)
        self.assertFalse(rulings[1].surplus)

    def test_find_rulings_lift_and_issue_decree(self):
        arrest_ref = "257647"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Ruling.LIFT.label, Ruling.ISSUES_DECREE.label], [ruling.ruling for ruling in rulings])
        self.assertFalse(rulings[0].surplus)
        self.assertFalse(rulings[1].surplus)

    def test_find_rulings_lift_and_reject(self):
        arrest_ref = "257985"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Ruling.LIFT.label, Ruling.REJECT.label], [ruling.ruling for ruling in rulings])
        self.assertFalse(rulings[0].surplus)
        self.assertFalse(rulings[1].surplus)

    def test_find_rulings_UNCOMPLETED_AND_REOPENING_DEBATES(self):
        arrest_ref = "257009"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Ruling.UNCOMPLETED.label, Ruling.REOPENING_DEBATES.label],
                         [ruling.ruling for ruling in rulings])
        self.assertFalse(rulings[0].surplus)
        self.assertFalse(rulings[1].surplus)

    def test_find_rulings_ordonne_2(self):
        arrest_ref = "257248"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Ruling.REJECT.label, Ruling.ORDERED.label], [ruling.ruling for ruling in rulings])
        self.assertTrue(rulings[0].surplus)
        self.assertFalse(rulings[1].surplus)

    def test_find_rulings_reopening_debates(self):
        arrest_ref = "257984"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(Ruling.REOPENING_DEBATES.label, rulings[0].ruling)
        self.assertFalse(rulings[0].surplus)

    def test_find_rulings_reject_2(self):
        arrest_ref = "258070"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual(Ruling.REJECT.label, rulings[0].ruling)
        self.assertFalse(rulings[0].surplus)

    def test_find_rulings_ordered_with_surplus_2(self):
        arrest_ref = "257081"
        reader = self.read_pdf(arrest_ref)
        rulings, error = self.rulingsFinder.find(arrest_ref, reader,
                                                 {self.rulingsFinder.IS_RECTIFIED_LABEL: False})
        self.assertEqual([Ruling.REJECT.label, Ruling.ORDERED.label], [ruling.ruling for ruling in rulings])
        self.assertTrue(rulings[0].surplus)
        self.assertFalse(rulings[1].surplus)

    def test_find_rulings_no_rectified_label(self):
        arrest_ref = "257081"
        reader = self.read_pdf(arrest_ref)
        with self.assertRaises(NotADirectoryError) as context:
            self.rulingsFinder.find(arrest_ref, reader)
        self.assertEqual("isRectified no in the dic", str(context.exception))
