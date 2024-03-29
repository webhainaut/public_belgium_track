# test_all.py
import unittest

from testarrest import TestArrest
from tests.arrest_finder.test_ArrestDateFinder import TestArrestDateFinder
from tests.arrest_finder.test_FinderAbstract import TestFinderAbstract
from testwebscraper import TestWebScraper

# Ajoutez toutes les classes de test que vous souhaitez exécuter
test_classes = [TestWebScraper, TestArrest, TestArrestDateFinder, TestFinderAbstract]

# Créez une suite de tests
test_suites = [unittest.TestLoader().loadTestsFromTestCase(test_classe) for test_classe in test_classes]

if __name__ == "__main__":
    # Exécutez la suite de tests
    [unittest.TextTestRunner().run(test_suite) for test_suite in test_suites]
