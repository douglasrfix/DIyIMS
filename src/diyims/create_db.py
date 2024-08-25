
#TODO: Create scripts to create db and tables with overrides

from pathlib import Path
import sqlite3
from sqlite3 import Error
import aiosql
from rich import print
from importlib import resources


def create():

    db_path = Path.home().joinpath('diyims.db')
    conn = sqlite3.connect(db_path)
    sql_str = resources.read_text("diyims.sql", "scripts.sql", encoding='utf-8', errors='strict')

    queries = aiosql.from_str(sql_str, "sqlite3")
    
    try:
        queries.create_schema(conn)
    except Error as e:
        print(f"The error '{e}' occurred.")
