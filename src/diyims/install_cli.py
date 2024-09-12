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
    ] = "Default",
    force_python: Annotated[
        bool, typer.Option(help="Force installation", rich_help_panel="Install Options")
    ] = False,
):
    """
    The installation process is intended to satisfy the needs of most users. That being said,
        there may be circumstances which result in error messages. The most common error may well be
        the error for an untested platform referring to Windows 10 or 11. This is because Microsoft
        introduced the
        Microsoft Store which is one option to install Python. Unfortunately, the behavior
        of how the system handles directories is different than if Python was installed from the
        Python.org but there is no method to detect source of the Python installation. An option
        --force-python has been provided to force the installer to accept the Python installation
        no matter the source.

    """
    install_app(drive_letter, force_python)


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
