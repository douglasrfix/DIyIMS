import typer
from diyims.beacon import purge_want_items
from diyims.scheduler import scheduler_main

app = typer.Typer(
    no_args_is_help=True, help="Execution of the Beacon function and subsets."
)


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
def beacon_operation():
    """
    Populates the Network_Peers table with a single entry to reflect this
    Network Node.
    If a pre-existing installation exists it will simply return with an error
    message
    """

    scheduler_main()
    return
