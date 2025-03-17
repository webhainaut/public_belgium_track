from typing import List

from main.models.models import ArrestModel
from tests.dao.testAbstract_dao import TestAbstractDao


class TestArrestDao(TestAbstractDao):

    def test_search_refs_and_bad_att(self):
        with self.assertRaises(ValueError) as context:
            self.arrestDao.search_refs_and(coucou="VI")
        self.assertEqual("Invalid parameter value: coucou=VI", str(context.exception))

    def test_search_refs_and_chamber(self):
        result = self.arrestDao.search_refs_and(chamber="VI")
        self.assertEqual([self.ref1, self.ref3], result)

    def test_search_refs_and_chamber_None(self):
        result = self.arrestDao.search_refs_and(chamber=None)
        self.assertEqual([self.ref2, self.ref4, self.ref5], result)

    def test_search_refs_and_chamber_2_args(self):
        result = self.arrestDao.search_refs_and(chamber="VI", pages=self.arrest1_pages)
        self.assertEqual([self.ref1], result)

    def test_search_refs_and_chamber_list(self):
        result = self.arrestDao.search_refs_and(chamber="VI", pages=[self.arrest1_pages, self.arrest3_pages])
        self.assertEqual([self.ref1, self.ref3], result)

    def test_get_arrest(self):
        arrest_result: ArrestModel = self.arrestDao.get(self.ref1)
        self.assertEqual(self.ref1, arrest_result.ref)
        self.assertEqual(self.suspension, arrest_result.procedures[0].process)
        self.assertEqual(self.ref1, arrest_result.procedures[0].arrest_ref)

    def test_get_last(self):
        arrest_result: ArrestModel = self.arrestDao.get_last()
        self.assertEqual(self.ref5, arrest_result.ref)

    def test_exist_arrest(self):
        self.assertTrue(self.arrestDao.exist(self.ref1))
        self.assertFalse(self.arrestDao.exist(657789))

    def test_update_arrest(self):
        new_pages = 7
        arrest_result: ArrestModel = self.arrestDao.get(self.ref1)
        self.assertEqual(self.ref1, arrest_result.ref)
        self.assertEqual(self.arrest1_pages, arrest_result.pages)
        self.assertNotEqual(new_pages, arrest_result.pages)

        arrest = ArrestModel(ref=self.ref1, language="fr", pages=new_pages, chamber="VII")
        self.arrestDao.update(arrest)
        arrest_result2: ArrestModel = self.arrestDao.get(self.ref1)
        self.assertEqual(new_pages, arrest_result2.pages)
        self.assertEqual("VII", arrest_result2.chamber)

    def test_get_arrests(self):
        arrest_results: List["ArrestModel"] = self.arrestDao.get_all([self.ref1, self.ref2])
        self.assertEqual(2, len(arrest_results))
        self.assertEqual(self.ref1, arrest_results[0].ref)
        self.assertEqual(self.ref2, arrest_results[1].ref)

    def test_get_arrests_last_year(self):
        arrest_results: List["ArrestModel"] = self.arrestDao.search_arrests_for_year(2024)
        self.assertEqual(2, len(arrest_results))
        self.assertEqual(self.ref2, arrest_results[0].ref)
        self.assertEqual(self.ref4, arrest_results[1].ref)
