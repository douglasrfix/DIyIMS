"""This is the command line interface driver.

It provides CLI access to each of the applications functions

It is part of an installable package so does not
need the if __name__ == "__main__":.

"""

import typer

from diyims import install_cli
from diyims import beacon_cli
from diyims.scheduler import scheduler_main
from diyims.ipfs_utils import force_purge
from diyims.ipfs_utils import purge
from diyims.peer_capture import (
    capture_providers_main,
    capture_bitswap_main,
    capture_swarm_main,
)
# from diyims.capture_want_lists import


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
def capture_providers():
    """Populates the Network_Peers table with a single entry to reflect this
    Network Node.
    If a pre-existing installation exists it will simply return with an error
    message
    """
    capture_providers_main()


# @app.command()
# def capture_want_lists():
#    process_peers()


@app.command()
def capture_swarm_peers():
    """Populates the Network_Peers table with a single entry to reflect this
    Network Node.
    If a pre-existing installation exists it will simply return with an error
    message
    """
    capture_swarm_main()


@app.command()
def capture_bitswap_peers():
    """Populates the Network_Peers table with a single entry to reflect this
    Network Node.
    If a pre-existing installation exists it will simply return with an error
    message
    """
    capture_bitswap_main()


@app.command()
def run_scheduler():
    """Populates the Network_Peers table with a single entry to reflect this
    Network Node.
    If a pre-existing installation exists it will simply return with an error
    message
    """
    scheduler_main()
