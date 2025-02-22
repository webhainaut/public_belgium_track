from typing import Annotated, List

import typer

from main.app.installer import Installer
from main.app.public_track_service import PublicTrackService

HELP_REFS = "suite de référence d'arrêt exemple : 255267"

app = typer.Typer(rich_markup_mode="rich")
public_track_service = PublicTrackService()

@app.command()
def bonjour():
    """
    Explique l'utilité de cette application
    """
    print(f"Bonjour, cette application permet à travers des différentes commandes \n"
          f"(et peut-être un jour de l'interface graphique) de traiter les arrêts \n"
          f"du conseil d'état qui se trouve sur : http://www.conseildetat.be")

@app.command()
def version():
    """
    Donne la version

    :avocado: :memo: :floppy_disk: :bell: :no_bell: :fox_face: :musical_keyboard: :musical_note: :book:
    :bookmark_tabs: :books: :tear-off_calendar: :date: :unicorn_face: :pencil: :classical_building: :printer:
    :fire:
    """
    print("Version 0.1")

@app.command()
def install():
    """
    Installe la base de donnée "public_belgium.db" dans de dossier "./dbs"
    [bold red]:warning: supprime la db si elle existe :warning:[/bold red]
    """
    Installer.install()

@app.command()
def download(refs: Annotated[List[int], typer.Argument(help=HELP_REFS)]):
    """Télécharge le(s) arrêts :scroll:"""
    public_track_service.download_all(refs)

@app.command()
def update(refs: Annotated[List[int], typer.Argument(help=HELP_REFS)]):
    """Mets à jour le(s) arrêts :scroll: (à n'utiliser que si le script a changé)"""
    public_track_service.update_all(refs)


if __name__ == "__main__":
    app()