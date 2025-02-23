import concurrent.futures
import logging
from typing import List

import pandas as pd

from main.Models.Models import ArrestModel
from main.dao.arrest_dao import ArrestDao
from main.dao.arrest_downloader import ArrestDownloader
from main.io.excel import Excel
from main.services.arrest_service import ArrestService
from main.services.webscraper import WebScraper

NB_CHUNKS = 1  # NB of threads


class PublicTrackService:

    def __init__(self):
        self.excel_writter = Excel()
        self.pd = pd
        self.web_scraper = WebScraper()
        self.arrest_downloader = ArrestDownloader()
        self.arrest_dao = ArrestDao()
        self.arrestService = ArrestService()
        self.logger = logging.getLogger(__name__)

    def download(self, ref):
        """va rechercher le pdf, traduit en ArrestModel et sauve le tout (pdf et arrest)"""
        if self.arrest_dao.exist(ref):
            self.logger.warning(f"arret {ref} existe déjà")
        else:
            try:
                pdf = self.web_scraper.find_arrest(ref)
                arrest = self.arrestService.get_arrest_from_pdf(ref, pdf)
                self.arrest_downloader.save_arrest(arrest, pdf)
                self.arrest_dao.add(arrest)
                self.logger.info(f"arret {ref} téléchargé")
            except Exception as e:
                self.logger.error(f"{e}")

    def download_latest(self):
        last_arrest: ArrestModel = self.arrest_dao.get_last()
        refs: List[int] = self.web_scraper.find_public_procurements_refs(last_ref=last_arrest.ref)
        if refs:
            self.download_all(refs)
        else:
            self.logger.info(f"Pas d'arrêt trouvé")

    def download_all(self, refs: List[int]):
        chunk_size = len(refs) // NB_CHUNKS + (
                len(refs) % NB_CHUNKS > 0)  # Assurez-vous que toutes les références sont traitées
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
                self.download(ref)
            except Exception as e:
                self.logger.error(f"Une erreur s'est produite pour {ref} : {e}")

    def update(self, ref):
        """Met à jour l'arrest en fonction des règles définie dans arrestService (utile si les règles change)"""
        if self.arrest_dao.exist(ref):
            arrest: ArrestModel = self.arrest_dao.get(ref)
            pdf = self.arrest_downloader.read_arrest(arrest)
            arrest_updated = self.arrestService.get_arrest_from_pdf(ref, pdf)
            self.arrest_downloader.move(arrest.get_path_to_pdf(), arrest_updated.get_path_to_pdf())
            self.arrest_dao.update(arrest_updated)
            self.logger.info(f"arret {ref} updated")
        else:
            self.logger.warning(f"arret {ref} n'existe pas")

    def update_all(self, refs: List[int]):
        chunk_size = len(refs) // NB_CHUNKS + (
                len(refs) % NB_CHUNKS > 0)  # Assurez-vous que toutes les références sont traitées
        chunks = [refs[i:i + chunk_size] for i in range(0, len(refs), chunk_size)]

        # Exécuter les téléchargements en parallèle
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Soumettre toutes les tâches
            futures = []
            for chunk in chunks:
                futures.append(executor.submit(self.update_chunk, chunk))

            # Attendre que toutes les tâches soient terminées
            for future in concurrent.futures.as_completed(futures):
                future.result()

    def update_chunk(self, chunk: List[int]):
        for ref in chunk:
            try:
                self.update(ref)
            except Exception as e:
                self.logger.error(f"Une erreur s'est produite pour {ref} : {e}")

    def update_year(self, year):
        arrests = self.arrest_dao.get_for_year(year)
        refs = [arrest.ref for arrest in arrests]
        self.update_all(refs)

    def read(self, ref: int):
        arrest: ArrestModel = self.arrest_dao.get(ref)
        if arrest is None:
            return None
        return self.pd.DataFrame([arrest.as_dict()])

    def read_all(self, refs):
        arrests:List[ArrestModel] = self.arrest_dao.get_all(refs)
        return self.pd.DataFrame([arrest.as_dict() for arrest in arrests])

    def read_year(self, year):
        arrests:List[ArrestModel] = self.arrest_dao.get_for_year(year)
        return self.pd.DataFrame([arrest.as_dict() for arrest in arrests])

    def add_to_excel(self, ref: int, file_name=None):
        arrest: ArrestModel = self.arrest_dao.get(ref)
        # S'assurer que l'arrêt est bien chargé...
        arrest.as_dict()
        self.excel_writter.add([arrest], file_name)

    def print_to_excel_all(self, refs, file_name=None):
        arrests:List[ArrestModel] = self.arrest_dao.get_all(refs)
        # S'assurer que les arrêts est bien chargé...
        [arrest.as_dict() for arrest in arrests]
        self.excel_writter.add(arrests, file_name)

    def print_to_excel_year(self, year, file_name=None):
        arrests:List[ArrestModel] = self.arrest_dao.get_for_year(year)
        # S'assurer que les arrêts est bien chargé...
        [arrest.as_dict() for arrest in arrests]
        self.excel_writter.add(arrests, file_name)
