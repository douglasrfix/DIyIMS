def get_sql_str9():
    from importlib import files

    sql_str = files("diyims.sql").joinpath("scripts.sql").read_text(encoding="utf-8")

    return sql_str


def get_car_path9():
    from importlib import files

    car_path = files("diyims.resources").joinpath("cartxt.txt").open("rb")

    return car_path
