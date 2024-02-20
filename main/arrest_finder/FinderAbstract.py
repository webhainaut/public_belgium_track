from abc import ABC, abstractmethod


class FinderAbstract(ABC):
    FIRST_TITLE_PATTERN = r'I\.\s*Objets*\s*(de\s*la|de\s*s|du)\s*(requête|recours)'
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
