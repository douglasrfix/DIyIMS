import typer
from rich import print

from diyims.database import create
from diyims.install import install_app

app = typer.Typer(no_args_is_help=True, help="Installation activities.")


@app.command()
def help():
    """This is to cath some of the looking form help attempts"""
    print("Try diyims install --help or diyims install ")


@app.command()
def install():
    """Installs the application files in preparation for initialization. If a pre-existing
    installation exists or some other problem occurs, it will simply return with an error message.
    """
    install_app()


@app.command()
def create_db():
    """Initializes the database to a known state. If a pre-existing
    installation exists it will simply return with an error message
    """
    create()
