#TODO: missing command yields default help text
#TODO: command and sub command help
#TODO: rationalize sub command names
#TODO: can this interface support support batch, command line and invoking from a windows application like file explorer?



import typer
from diyims.create_db import create

app = typer.Typer()

@app.command()
def main(name: str):
    print(f"Hello {name}")

@app.command()
def createdb():
    create()

def run():
    app()


