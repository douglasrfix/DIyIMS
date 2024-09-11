# TODO: enhance command help

"""  This is the command line interface driver.

     It provides CLI access to each of the applications functions

     It is part of an installable package so does not
     need the if __name__ == "__main__":.

"""

import typer
from rich import print

from diyims import install_cli

app = typer.Typer(
    no_args_is_help=True, help="Base command for the DIY Independent Media Services."
)
# app.add_typer(database_cli.app, name="database")
# app.add_typer(configuration_cli.app, name="config")
app.add_typer(install_cli.app, name="install")


@app.command()
def help():
    """This is to cath some of the looking for help attempts"""
    print("Try diyims --help or just diyims")
