"""  This is the command line interface driver.

     It provides CLI access to each of the applications functions

     It is part of an installable package so does not
     need the if __name__ == "__main__":.

"""

import typer

from diyims import install_cli

app = typer.Typer(
    no_args_is_help=True, help="Base command for the DIY Independent Media Services."
)
# app.add_typer(database_cli.app, name="database")
# app.add_typer(configuration_cli.app, name="config")
app.add_typer(install_cli.app, name="install-utils")
