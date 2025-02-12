import logging

from pypdf import PdfReader

from main.Models.Models import ArrestModel

DEFAULT_ARREST_PDF = "{directory}/{ref}.pdf"
DEFAULT_ARRESTS_DIRECTORY = "{chamber}/{year}/{month}"

class ArrestDownloader:
    logging.basicConfig(level=logging.ERROR)

    @staticmethod
    def download_arrest(arrest: ArrestModel, pdf):
        if arrest.path_to_pdf is None:
            path = DEFAULT_ARRESTS_DIRECTORY.format(chamber=arrest.chamber, year=arrest.arrest_date.year,
                                                    month=arrest.arrest_date.month)
            arrest.path_to_pdf = DEFAULT_ARREST_PDF.format(directory=path, ref=arrest.ref)
        with open(arrest.path_to_pdf, mode="wb") as file:
            file.write(pdf)

    @staticmethod
    def read_arrest(arrest: ArrestModel):
        if arrest.path_to_pdf is None:
            path = DEFAULT_ARRESTS_DIRECTORY.format(chamber=arrest.chamber, year=arrest.arrest_date.year,
                                                    month=arrest.arrest_date.month)
            arrest.path_to_pdf = DEFAULT_ARREST_PDF.format(directory=path, ref=arrest.ref)
        return PdfReader(arrest.path_to_pdf)
