import os

from jproperties import Properties


class LocalProperties:
    DEFAULT_PATH = 'ressources/app-config.properties'

    def __init__(self, path=DEFAULT_PATH):
        self.configs = Properties()
        with open(os.path.abspath(os.path.dirname(__file__)) + "/../../" + path, 'rb') as config_file:
            self.configs.load(config_file)

    def get(self, key):
        return self.configs.get(key).data
