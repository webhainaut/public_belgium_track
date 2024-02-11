from main.arrest_finder.ArrestDateFinder import ArrestDateFinder
from main.arrest_finder.AskProcessFinder import AskProcessFinder
from main.arrest_finder.IsRectifiedFinder import IsRectifiedFinder
from main.arrest_finder.RoleNumberFinder import RoleNumberFinder


class ArrestFinder:
    def __init__(self):
        self.isRectifiedFinder = IsRectifiedFinder('Rectifié')
        self.arrestDateFinder = ArrestDateFinder('Date de l\'arrêt')
        self.askProcessFinder = AskProcessFinder('Demande de procédure')
        self.roleNumberFinder = RoleNumberFinder('N° de Rôle')
