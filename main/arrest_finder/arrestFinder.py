from main.arrest_finder.arrestDateFinder import ArrestDateFinder
from main.arrest_finder.askProcessFinder import AskProcessFinder
from main.arrest_finder.chamberFinder import ChamberFinder
from main.arrest_finder.isRectifiedFinder import IsRectifiedFinder
from main.arrest_finder.keywordsFinder import KeywordsFinder
from main.arrest_finder.casesFinder import CasesFinder
from main.arrest_finder.rulingsFinder import RulingsFinder


class ArrestFinder:
    def __init__(self):
        self.casesFinder = CasesFinder('N° de Rôle')
        self.isRectifiedFinder = IsRectifiedFinder('Rectifié')
        self.arrestDateFinder = ArrestDateFinder('Date de l\'arrêt')
        self.askProcessFinder = AskProcessFinder('Demande de procédure')
        self.rulingsFinder = RulingsFinder('Décision')
        self.keywordsFinder = KeywordsFinder('Keywords')
        self.chamberFinder = ChamberFinder('Chamber')
