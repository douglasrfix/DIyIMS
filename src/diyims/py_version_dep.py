import sys


def get_sql_str():
    if sys.version_info[1] == 8:
        from importlib import resources

        sql_str = resources.read_text(
            "diyims.sql", "scripts.sql", encoding="utf-8", errors="strict"
        )
    else:
        # NOTE: requires testing under python > 3.8
        from importlib.resources import files

        sql_str = (
            files("diyims.sql").joinpath("scripts.sql").read_text(encoding="utf-8")
        )

    return sql_str


def get_car_path():
    if sys.version_info[1] == 8:
        from importlib import resources

        car_path = resources.open_binary("diyims.resources", "cartext.car")

    else:
        from importlib.resources import files

        car_path = files("diyims.resources").joinpath("cartext.car").open("rb")

    return car_path
