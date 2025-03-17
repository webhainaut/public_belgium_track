from main.Models.ModelsDao import CaseModelDao, ArrestModelDao
from main.dao.case_dao import CaseDao
from tests.dao.testAbstract_dao import TestAbstractDao


class TestCaseDao(TestAbstractDao):

    def setUp(self):
        super().setUp()
        self.caseDao = CaseDao()
        self.ref = 112477

    def test_get(self):
        case: CaseModelDao = self.caseDao.get(self.numRole1)
        self.assertEqual(self.ref1, case.arrests[0].ref)
        self.assertEqual(self.numRole1, case.numRole)

    def test_add_arrest_with_case(self):
        case: CaseModelDao = self.caseDao.get(self.numRole1)
        self.assertEqual(1, len(case.arrests))
        self.assertFalse(self.arrestDao.exist(self.ref), "arrest not exist before we try to add")
        merged_case = self.arrestDao.session.merge(case)

        new_arrest = ArrestModelDao(ref=self.ref, language="fr", chamber="VI", cases=[merged_case])
        self.arrestDao.add(new_arrest)

        self.arrestDao.session.refresh(merged_case)
        self.assertEqual(2, len(merged_case.arrests))
        self.caseDao.session.close()
        case2: CaseModelDao = self.caseDao.get(self.numRole1)
        self.assertEqual(2, len(case2.arrests))

