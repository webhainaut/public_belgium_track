# test_all.py
import unittest

from tests.arrest_finder.test_ArrestDateFinder import TestArrestDateFinder
from testwebscraper import TestWebScraper
from testarrest import TestArrest

# Ajoutez toutes les classes de test que vous souhaitez exécuter
test_classes = [TestWebScraper, TestArrest, TestArrestDateFinder]

# Créez une suite de tests
test_suites = [unittest.TestLoader().loadTestsFromTestCase(test_classe) for test_classe in test_classes]

if __name__ == "__main__":
    # Exécutez la suite de tests
    [unittest.TextTestRunner().run(test_suite) for test_suite in test_suites]
