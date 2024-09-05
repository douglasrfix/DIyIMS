import typer
from rich import print

from diyims.init_db_env import init

app = typer.Typer(no_args_is_help=True, help="Database activities.")


@app.command()
def help():
    """This is to cath some of the looking form help attempts"""
    print("Try --help or diyims ")


@app.command()
def init_db():
    """Populates the Network_Peers table with a single entry to reflect this
    Network Node.
    If a pre-existing installation exists it will simply return with an error
    message

    """
    init()
