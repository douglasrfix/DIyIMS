"""
    A tuple containing the five components of the version number: major, minor, micro, releaselevel, and serial.
    All values except releaselevel are integers; the release level is 'alpha', 'beta', 'candidate', or 'final'.
    The version_info value corresponding to the Python version 2.0 is (2, 0, 0, 'final', 0).
    The components can also be accessed by name, so sys.version_info[0] is equivalent to
    sys.version_info.major and so on.
"""
import sys

from diyims.import_lib9 import get_car_path9, get_sql_str9


def get_sql_str():
    if sys.version_info.minor == 8:
        from importlib import resources

        sql_str = resources.read_text(
            "diyims.sql", "scripts.sql", encoding="utf-8", errors="strict"
        )
    else:
        print(sys.version_info)
        sql_str = get_sql_str9()

    return sql_str


def get_car_path():
    if sys.version_info.minor == 8:
        from importlib import resources

        car_path = resources.open_binary("diyims.resources", "cartext.car")

    else:
        car_path = get_car_path9()

    return car_path
