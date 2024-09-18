from importlib import resources


def get_sql_str():
    sql_str = resources.read_text(
        "diyims.sql", "scripts.sql", encoding="utf-8", errors="strict"
    )
    return sql_str
