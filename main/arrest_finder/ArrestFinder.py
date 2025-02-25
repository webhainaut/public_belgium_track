from main.arrest_finder.ArrestDateFinder import ArrestDateFinder
from main.arrest_finder.AskProcessFinder import AskProcessFinder
from main.arrest_finder.ChamberFinder import ChamberFinder
from main.arrest_finder.IsRectifiedFinder import IsRectifiedFinder
from main.arrest_finder.KeywordsFinder import KeywordsFinder
from main.arrest_finder.CasesFinder import CasesFinder
from main.arrest_finder.RulingsFinder import RulingsFinder


class ArrestFinder:
    def __init__(self):
        self.casesFinder = CasesFinder('N° de Rôle')
        self.isRectifiedFinder = IsRectifiedFinder('Rectifié')
        self.arrestDateFinder = ArrestDateFinder('Date de l\'arrêt')
        self.askProcessFinder = AskProcessFinder('Demande de procédure')
        self.rulingsFinder = RulingsFinder('Décision')
        self.keywordsFinder = KeywordsFinder('Keywords')
        self.chamberFinder = ChamberFinder('Chamber')
