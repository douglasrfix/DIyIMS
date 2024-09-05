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
from diyims import configuration_cli, database_cli, install_cli

app = typer.Typer(no_args_is_help=True, help="Awesome CLI user manager.")
app.add_typer(database_cli.app, name="database")
app.add_typer(configuration_cli.app, name="config")
app.add_typer(install_cli.app, name="install")


@app.command()
def help():
    """This is to cath some of the looking for help attempts"""
    print("Try diyims --help or just diyims")
