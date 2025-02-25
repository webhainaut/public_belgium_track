import logging
from datetime import datetime
from typing import Annotated, List, Optional

import typer

from main.app.installer import Installer
from main.app.public_track_service import PublicTrackService

HELP_REFS = "suite de référence d'arrêt exemple : 255267"

app = typer.Typer(rich_markup_mode="rich")
installer = Installer()
public_track_service = PublicTrackService()
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


@app.command()
def bonjour():
    """
    Explique l'utilité de cette application
    """
    typer.echo(f"Bonjour, cette application permet à travers des différentes commandes \n"
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
    typer.echo(f"Version 0.1")


@app.command()
def install(force: bool = typer.Option(False, "--force", "-f",
                                       help="Forcer la réinstallation même si la base de données existe déjà")):
    """
    Installe la base de données "public_belgium.db" dans le dossier "./dbs"
    """
    typer.secho("/!\\ Cette opération supprimera la base de données existante si elle existe", fg=typer.colors.RED)

    if not force and installer.db_exists():
        typer.confirm("La base de données existe déjà. Voulez-vous la réinstaller ?", abort=True)

    installer.install()
    typer.secho("Installation terminée avec succès !", fg=typer.colors.GREEN, bold=True)


@app.command()
def download(refs: Annotated[List[int], typer.Argument(help=HELP_REFS)] = None,
             latest: Annotated[bool, typer.Option("--latest", "-l", help="Télécharger les derniers arrêts")] = False):
    """Télécharge le(s) arrêt(s) spécifié(s) ou les plus récents :scroll:"""
    try:
        if latest and refs is None:
            public_track_service.download_latest()
            typer.echo("Les derniers arrêts ont été téléchargés avec succès.")
        elif refs and not latest:
            public_track_service.download_all(refs)
            typer.echo(f"Les arrêts avec les références {refs} ont été téléchargés.")
        else:
            raise typer.BadParameter("Il faut soit une liste de refs, soit utiliser l'option --latest")
    except Exception as e:
        typer.echo(f"Erreur lors du téléchargement des arrêts : {str(e)}", err=True)
        raise typer.Exit(code=1)


@app.command(name="print")
def print_excel_years(year: Annotated[
    int, typer.Argument(help="Année pour laquelle imprimer les arrêts", min=1900, max=datetime.now().year)],
                      file_name: Annotated[Optional[str], typer.Option(help="Nom du fichier de sortie")] = "result"):
    """
    Ajoute les arrêts de l'année spécifiée dans l'excel :book: :printer:
    """
    try:
        public_track_service.print_to_excel_by_year(year, file_name)
        typer.echo(f"Les arrêts de l'année {year} ont été ajoutés au fichier '{file_name}'.")
    except Exception as e:
        typer.echo(f"Erreur lors de l'impression des arrêts : {str(e)}")
        raise typer.Exit(code=1)


@app.command(name="print-refs")
def print_excel_refs(refs: Annotated[List[int], typer.Argument(help=HELP_REFS)], file_name="result"):
    """
    Ajoute les arrêts dans l'excel :book: :printer:
    """
    public_track_service.print_to_excel_all(refs, file_name)


@app.command()
def read(refs: Annotated[List[int], typer.Argument(help=HELP_REFS)]):
    """
    Affiche les arrêts spécifiés par leurs références :memo:
    """
    try:
        result = public_track_service.read_all(refs)
        typer.echo(result)
    except Exception as e:
        typer.echo(f"Erreur lors de la lecture des arrêts : {str(e)}", err=True)
        raise typer.Exit(code=1)



if __name__ == "__main__":
    app()
