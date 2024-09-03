# TODO: 0.0.0a1 introduce sub command
# TODO: > 0.0.0a0 can this interface support support batch, command line and
#   invoking
#   from a windows application like file explorer?
# TODO: > 0.0.0a0 powershell variable $Error to see stderr output on the
#   console.

"""  This is the command line interface driver.

     It provides CLI access to each of the applications functions

     It is part of an installable package so does not
     need the if __name__ == "__main__":.

"""

import typer
from rich import print

# from diyims.config import config
from diyims.init_db_env import create, init, test

app = typer.Typer(no_args_is_help=True, help="Awesome CLI user manager.")


@app.command()
def help():
    """This is to cath some of the looking form help attempts"""
    print("Try --help or diyims ")


@app.command()
def create_db():
    """Initializes the database to a known state. If a pre-existing
    installation exists it will simply return with an error message
    """
    create()


@app.command()
def init_app():
    """Populates the Network_Peers table with a single entry to reflect this
    Network Node.
    If a pre-existing installation exists it will simply return with an error
    message

    """
    init()


'''
@app.command()
def config_app():
    """Populates the Network_Peers table with a single entry to reflect this
    Network Node.
    If a pre-existing installation exists it will simply return with an error
    message

    """
    config()

'''


@app.command()
def test_app():
    """Populates the Network_Peers table with a single entry to reflect this
    Network Node.
    If a pre-existing installation exists it will simply return with an error
    message

    """
    test()
