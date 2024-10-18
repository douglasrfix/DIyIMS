import aiosql

from diyims.py_version_dep import get_sql_str


def insert_peer_row(conn, peer_table_dict):
    sql_str = get_sql_str()
    queries = aiosql.from_str(sql_str, "sqlite3")

    queries.insert_peer_row(
        conn,
        peer_table_dict["peer_ID"],
        peer_table_dict["IPNS_name"],
        peer_table_dict["origin_update_DTS"],
        peer_table_dict["local_update_DTS"],
        peer_table_dict["execution_platform"],
        peer_table_dict["python_version"],
        peer_table_dict["IPFS_agent"],
        peer_table_dict["processing_status"],
        peer_table_dict["agent"],
        peer_table_dict["version"],
    )
    return


def insert_network_row(conn, network_table_dict):
    sql_str = get_sql_str()
    queries = aiosql.from_str(sql_str, "sqlite3")

    queries.insert_network_row(
        conn,
        network_table_dict["network_name"],
    )
    return


def insert_want_list_row(conn, want_list_table_dict):
    sql_str = get_sql_str()
    queries = aiosql.from_str(sql_str, "sqlite3")

    queries.insert_want_list_row(
        conn,
        want_list_table_dict["peer_ID"],
        want_list_table_dict["object_CID"],
    )
    return
