from typing import Optional

import typer
from typing_extensions import Annotated
from diyims.beacon_utils import create_beacon_CID, non_multi_flash, purge_want_items
from diyims.worker_multi import main

app = typer.Typer(
    no_args_is_help=True, help="Execution of the Beacon function and subsets."
)


@app.command()
def beacon_CID():
    """Populates the Network_Peers table with a single entry to reflect this
    Network Node.
    If a pre-existing installation exists it will simply return with an error
    message
    """
    create_beacon_CID()
    return


@app.command()
def partial_beacon():
    """Populates the Network_Peers table with a single entry to reflect this
    Network Node.
    If a pre-existing installation exists it will simply return with an error
    message
    """
    non_multi_flash()
    return


@app.command()
def purge_beacon_files():
    """Populates the Network_Peers table with a single entry to reflect this
    Network Node.
    If a pre-existing installation exists it will simply return with an error
    message
    """
    purge_want_items()
    return


@app.command()
def beacon_test(
    minutes_to_run: Annotated[
        Optional[str],
        typer.Option(
            help="How many minutes to run before normal shutdown.",
            show_default=True,
            rich_help_panel="Beacon Options",
        ),
    ] = "Default",
    long_period_seconds: Annotated[
        Optional[str],
        typer.Option(
            help="How long in seconds is the 'long' flash of the beacon.",
            show_default=True,
            rich_help_panel="Beacon Options",
        ),
    ] = "Default",
    short_period_seconds: Annotated[
        Optional[str],
        typer.Option(
            help="How long in seconds is the 'short' flash of the beacon.",
            show_default=True,
            rich_help_panel="Beacon Options",
        ),
    ] = "Default",
    number_of_periods: Annotated[
        Optional[str],
        typer.Option(
            help="How many flashes before the long is replaced by the short flash .",
            show_default=True,
            rich_help_panel="Beacon Options",
        ),
    ] = "Default",
):
    """
    Populates the Network_Peers table with a single entry to reflect this
    Network Node.
    If a pre-existing installation exists it will simply return with an error
    message
    """

    main(minutes_to_run, long_period_seconds, short_period_seconds, number_of_periods)
    return
