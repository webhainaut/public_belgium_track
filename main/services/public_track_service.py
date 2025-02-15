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

    def download_arrest(self, ref):
        """va rechercher le pdf, traduit en ArrestModel et sauve le tout (pdf et arrest)"""
        pdf = self.web_scraper.find_arrest(ref)
        arrest = self.arrestService.get_arrest_from_pdf(ref, pdf)
        self.arrest_downloader.save_arrest(arrest, pdf)
        self.arrest_dao.add_arrest(arrest)
