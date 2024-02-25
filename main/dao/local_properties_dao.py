import os

from jproperties import Properties


class LocalProperties:

    def __init__(self, path='ressources/app-config.properties'):
        self.configs = Properties()
        with open(os.path.abspath(os.path.dirname(__file__)) + "/../../" + path, 'rb') as config_file:
            self.configs.load(config_file)

    def get(self, key):
        return self.configs.get(key).data
