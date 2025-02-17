import concurrent.futures
import logging
from typing import List

from main.dao.arrest_dao import ArrestDao
from main.dao.arrest_downloader import ArrestDownloader
from main.services.arrest_service import ArrestService
from main.services.webscraper import WebScraper

NB_CHUNKS = 1 # NB of threads

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

    def download_in_parallel(self, refs: List[int]):
        chunk_size = len(refs) // NB_CHUNKS + (len(refs) % NB_CHUNKS > 0)  # Assurez-vous que toutes les références sont traitées
        chunks = [refs[i:i + chunk_size] for i in range(0, len(refs), chunk_size)]

        # Exécuter les téléchargements en parallèle
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Soumettre toutes les tâches
            futures = []
            for chunk in chunks:
                futures.append(executor.submit(self.download_chunk, chunk))

            # Attendre que toutes les tâches soient terminées
            for future in concurrent.futures.as_completed(futures):
                future.result()

    def download_chunk(self, chunk: List[int]):
        for ref in chunk:
            try:
                self.download_arrest(ref)
            except Exception as e:
                self.logger.error(f"Une erreur s'est produite pour {ref} : {e}")

