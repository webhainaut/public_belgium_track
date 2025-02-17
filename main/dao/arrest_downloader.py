import logging
import os

from pypdf import PdfReader

from main.Models.Models import ArrestModel


class ArrestDownloader:

    def __init__(self):
        self.os = os
        self.logger = logging.getLogger(__name__)

    def save_arrest(self, arrest: ArrestModel, pdf):
        if arrest.path is None:
            arrest.set_path()
        if not self.os.path.exists(arrest.path):
            self.os.makedirs(arrest.path)
        with open(arrest.get_path_to_pdf(), mode="wb") as file:
            file.write(pdf)

    @staticmethod
    def read_arrest(arrest: ArrestModel):
        if arrest.path is None:
            arrest.set_path()
        return PdfReader(arrest.get_path_to_pdf())
