import sys
from importlib import resources

from diyims.import_lib9 import get_sql_str9, get_car_path9


def get_sql_str():
    if sys.version_info[1] == 8:
        sql_str = resources.read_text(
            "diyims.sql", "scripts.sql", encoding="utf-8", errors="strict"
        )
    else:
        sql_str = get_sql_str9()

    return sql_str


def get_car_path():
    if sys.version_info[1] == 8:
        car_path = resources.open_binary("diyims.resources", "cartxt.car")

    else:
        car_path = get_car_path9()

    return car_path
