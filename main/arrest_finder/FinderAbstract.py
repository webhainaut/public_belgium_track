import logging
from abc import ABC, abstractmethod

from main.Exceptions.DataNotFoundException import DataNotFoundException


class FinderAbstract(ABC):
    FIRST_TITLE_PATTERN = r'I\.\s*Objets*\s*(de\s*la|de\s*s|du)\s*(requ(ê|e)te|recours)'
    RULING_PATTERN = (r"L\s*E\s*C\s*O\s*N\s*S\s*E\s*I\s*L\s*D\s*(’|')\s*("
                      r"É|E)\s*T\s*A\s*T\s*D\s*É\s*C\s*I\s*D\s*E\s*.*\s*:")
    IS_RECTIFIED_LABEL = 'isRectified'

    def __init__(self, service):
        self.service = service
        self.logger = logging.getLogger(__name__)

    def find(self, ref, reader, args=None):
        """Find data from Arrest file"""
        self._check_args_contains(args)
        try:
            data = self._find_data(ref, reader, args)
        except DataNotFoundException as e:
            return None, e.message
        return data, None


    @abstractmethod
    def _check_args_contains(self, args):
        """
        Contrainte pour s'assurer que les arguments a passer à la fonction sont bien présent.
        Exemple, vérifie qu'on aie bien l'information si l'arret est rectifier (si "IS_RECTIFIED_LABEL" est présent)
        IS_RECTIFIED_LABEL est ensuite utiliser pour récupérer la première page de l'arret
        """
        pass

    @abstractmethod
    def _find_data(self, ref, reader, args):
        pass
