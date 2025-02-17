import logging

from main.dao.arrest_dao import ArrestDao
from main.dao.arrest_downloader import ArrestDownloader
from main.services.arrest_service import ArrestService
from main.services.webscraper import WebScraper


class PublicTrackService:

    def __init__(self):
        self.web_scraper = WebScraper()
        self.arrest_downloader = ArrestDownloader()
        self.arrest_dao = ArrestDao()
        self.arrestService = ArrestService()
        self.logger = logging.getLogger(__name__)

    def download_arrest(self, ref):
        """va rechercher le pdf, traduit en ArrestModel et sauve le tout (pdf et arrest)"""
        if self.arrest_dao.arrest_exist(ref):
            self.logger.warning(f"arret {ref} existe déjà")
        else:
            pdf = self.web_scraper.find_arrest(ref)
            arrest = self.arrestService.get_arrest_from_pdf(ref, pdf)
            self.arrest_downloader.save_arrest(arrest, pdf)
            self.arrest_dao.add_arrest(arrest)
            self.logger.info(f"arret {ref} téléchargé")
