from typing import Optional

import typer
from rich import print
from typing_extensions import Annotated

from diyims.database import create, init
from diyims.install import install_app

app = typer.Typer(no_args_is_help=True, help="Installation activities.")


@app.command()
def help():
    """This is to cath some of the looking form help attempts"""
    print("Try diyims install --help or diyims install ")


@app.command()
def install(
    drive_letter: Annotated[
        Optional[str],
        typer.Option(
            help="The drive letter to use if not the default eg 'C'.",
            show_default=False,
            rich_help_panel="Install Options",
        ),
    ] = "Default"
):
    """
    The path that will be used to locate the database. This is in the form of the platform
    the application is installed upon.

    installation exists or some other problem occurs, it will simply return with an error message.
    """
    install_app(drive_letter)


@app.command()
def create_db():
    """Initializes the database to a known state. If a pre-existing
    installation exists it will simply return with an error message
    """
    create()


@app.command()
def init_db():
    """Populates the Network_Peers table with a single entry to reflect this
    Network Node.
    If a pre-existing installation exists it will simply return with an error
    message

    """
    init()
