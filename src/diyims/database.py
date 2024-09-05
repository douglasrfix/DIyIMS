import configparser
import sqlite3
from importlib import resources
from pathlib import Path
from sqlite3 import Error

import aiosql
from rich import print


def create():
    ini_path = Path.home().joinpath("AppData", "Local", "diyims", "diyims.ini")
    config = configparser.ConfigParser()
    config.sections()
    config.read(ini_path)
    db_path = config["Paths"]["db_path"]

    sql_str = resources.read_text(
        "diyims.sql", "scripts.sql", encoding="utf-8", errors="strict"
    )
    connect_path = Path.joinpath(db_path, "diyims.db")
    conn = sqlite3.connect(connect_path)

    queries = aiosql.from_str(sql_str, "sqlite3")

    try:
        queries.create_schema(conn)
        print("DB Schema creation successful.")
    except Error as e:
        print(f"The error '{e}' occurred.")

    conn.close()
