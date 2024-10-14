"""  This is the command line interface driver.

     It provides CLI access to each of the applications functions

     It is part of an installable package so does not
     need the if __name__ == "__main__":.

"""

import typer

from diyims import install_cli
from diyims.ipfs_utils import purge

# from diyims.find_providers import get_providers

app = typer.Typer(
    no_args_is_help=True, help="Base command for the DIY Independent Media Services."
)
# app.add_typer(database_cli.app, name="database")
# app.add_typer(configuration_cli.app, name="config")
app.add_typer(install_cli.app, name="install-utils")


"""
@app.command()
def experiment():
    Populates the Network_Peers table with a single entry to reflect this
    Network Node.
    If a pre-existing installation exists it will simply return with an error
    message

    test()
"""


@app.command()
def ipfs_purge():
    """
    ipfs purge for test cid.

    """
    purge()

    '''
    @app.command()
    def get_providers():
    """Populates the Network_Peers table with a single entry to reflect this
    Network Node.
    If a pre-existing installation exists it will simply return with an error
    message

    """
    get_providers()
    '''
