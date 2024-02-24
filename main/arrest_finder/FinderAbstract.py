from abc import ABC, abstractmethod


class FinderAbstract(ABC):
    FIRST_TITLE_PATTERN = r'I\.\s*Objets*\s*(de\s*la|de\s*s|du)\s*(requête|recours)'
    RULING_PATTERN = (r"L\s*E\s*C\s*O\s*N\s*S\s*E\s*I\s*L\s*D\s*(’|')\s*("
                      r"É|E)\s*T\s*A\s*T\s*D\s*É\s*C\s*I\s*D\s*E\s*.*\s*:")
    IS_RECTIFIED_LABEL = 'isRectified'

    def __init__(self, service):
        self.service = service

    def find(self, ref, reader, args=None):
        """Find data from Arrest file"""
        self._check_args_contains(args)
        data = self._find_data(ref, reader, args)
        return data

    @abstractmethod
    def _check_args_contains(self, args):
        pass

    @abstractmethod
    def _find_data(self, ref, reader, args):
        pass
