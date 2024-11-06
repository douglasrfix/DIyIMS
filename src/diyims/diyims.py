"""This is the command line interface driver.

It provides CLI access to each of the applications functions

It is part of an installable package so does not
need the if __name__ == "__main__":.

"""

import typer
from typing_extensions import Annotated
from typing import Optional

from diyims import install_cli
from diyims import beacon_cli

from diyims.capture_want_lists import get_remote_peers

from diyims.find_providers import get_providers
from diyims.ipfs_utils import force_purge, purge
from diyims.research_utils import get_bitswap_stat, get_swarm_peers


app = typer.Typer(
    no_args_is_help=True, help="Base command for the DIY Independent Media Services."
)
# app.add_typer(database_cli.app, name="database")
# app.add_typer(configuration_cli.app, name="config")
app.add_typer(install_cli.app, name="install-utils")
app.add_typer(beacon_cli.app, name="beacon-utils")


@app.command()
def danger():
    """
    Populates the Network_Peers table with a single entry to reflect this
    Network Node.
    If a pre-existing installation exists it will simply return with an error
    message
    """

    force_purge()


@app.command()
def ipfs_purge():
    """
    ipfs purge for test cid.

    """
    purge()


@app.command()
def find_providers():
    """Populates the Network_Peers table with a single entry to reflect this
    Network Node.
    If a pre-existing installation exists it will simply return with an error
    message
    """
    get_providers()


@app.command()
def capture_want_lists(
    ten_second_intervals: Annotated[
        Optional[int],
        typer.Option(
            help="The drive letter to use if not the default eg 'C:', note the colon.",
            show_default=True,
            rich_help_panel="Install Options",
        ),
    ] = 60,
):
    """Populates the Network_Peers table with a single entry to reflect this
    Network Node.
    If a pre-existing installation exists it will simply return with an error
    message
    """
    get_remote_peers(ten_second_intervals)


@app.command()
def want_list_stats():
    """Populates the Network_Peers table with a single entry to reflect this
    Network Node.
    If a pre-existing installation exists it will simply return with an error
    message
    """
    get_bitswap_stat()


@app.command()
def want_list_swarm():
    """Populates the Network_Peers table with a single entry to reflect this
    Network Node.
    If a pre-existing installation exists it will simply return with an error
    message
    """
    get_swarm_peers()
