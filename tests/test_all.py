# test_all.py
import unittest

from tests.models.test_converterModel import TestConverterModel
from tests.arrest_finder.test_AskProcessFinder import TestAskProcessFinder
from tests.arrest_finder.test_CasesFinder import TestCasesFinder
from tests.arrest_finder.test_ArrestDateFinder import TestArrestDateFinder
from tests.arrest_finder.test_ChamberFinder import TestChamberFinder
from tests.arrest_finder.test_FinderService import TestFinderService
from tests.arrest_finder.test_KeywordsFinder import TestKeywordsFinder
from tests.arrest_finder.test_RulingsFinder import TestRulingsFinder
from tests.dao.test_arrest_dao import TestArrestDao
from tests.services.test_arrest_service import TestArrestService
from tests.services.test_webscraper import TestWebScraper

# Ajoutez toutes les classes de test que vous souhaitez exécuter
test_classes = [TestArrestDao, TestWebScraper, TestArrestDateFinder, TestFinderService, TestRulingsFinder,
                TestKeywordsFinder, TestArrestService, TestChamberFinder, TestConverterModel, TestCasesFinder,
                TestAskProcessFinder]

# Créez une suite de tests
test_suites = [unittest.TestLoader().loadTestsFromTestCase(test_classe) for test_classe in test_classes]

if __name__ == "__main__":
    # Exécutez la suite de tests
    [unittest.TextTestRunner().run(test_suite) for test_suite in test_suites]
