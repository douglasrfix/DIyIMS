import aiosql

from diyims.py_version_dep import get_sql_str


def insert_peer_row(conn, peer_table_dict):
    sql_str = get_sql_str()
    queries = aiosql.from_str(sql_str, "sqlite3")

    queries.insert_peer_row(
        conn,
        peer_table_dict["peer_ID"],
        peer_table_dict["IPNS_name"],
        peer_table_dict["peer_type"],
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


def refresh_peer_table_dict():
    peer_table_dict = {}
    peer_table_dict["peer_ID"] = "null"
    peer_table_dict["IPNS_name"] = "null"
    peer_table_dict["peer_type"] = "null"
    peer_table_dict["origin_update_DTS"] = "null"
    peer_table_dict["local_update_DTS"] = "null"
    peer_table_dict["execution_platform"] = "null"
    peer_table_dict["python_version"] = "null"
    peer_table_dict["IPFS_agent"] = "null"
    peer_table_dict["processing_status"] = "null"
    peer_table_dict["version"] = "0"
    peer_table_dict["agent"] = "diyims/0.0.0"
    return peer_table_dict


def insert_network_row(conn, network_table_dict):
    sql_str = get_sql_str()
    queries = aiosql.from_str(sql_str, "sqlite3")

    queries.insert_network_row(
        conn,
        network_table_dict["network_name"],
    )
    return


def refresh_network_table_dict():
    network_table_dict = {}
    network_table_dict["version"] = "0"
    network_table_dict["network_name"] = "null"
    return network_table_dict


def insert_want_list_row(conn, queries, want_list_table_dict):
    # sql_str = get_sql_str()
    # queries = aiosql.from_str(sql_str, "sqlite3")

    queries.insert_want_list_row(
        conn,
        want_list_table_dict["peer_ID"],
        want_list_table_dict["object_CID"],
        want_list_table_dict["insert_DTS"],
        want_list_table_dict["last_update_DTS"],
        want_list_table_dict["insert_update_delta"],
        want_list_table_dict["source_peer_type"],
    )
    return


def update_last_update_DTS(conn, queries, want_list_table_dict):
    # sql_str = get_sql_str()
    # queries = aiosql.from_str(sql_str, "sqlite3")

    queries.update_last_update_DTS(
        conn,
        want_list_table_dict["last_update_DTS"],
        want_list_table_dict["insert_update_delta"],
        want_list_table_dict["peer_ID"],
        want_list_table_dict["object_CID"],
    )
    return


def select_want_list_entry_by_key(conn, queries, want_list_table_dict):
    # sql_str = get_sql_str()
    # queries = aiosql.from_str(sql_str, "sqlite3")

    want_list_entry = queries.select_want_list_entry_by_key(
        conn,
        want_list_table_dict["peer_ID"],
        want_list_table_dict["object_CID"],
    )
    return want_list_entry


def refresh_want_list_table_dict():
    want_list_table_dict = {}
    want_list_table_dict["peer_ID"] = "null"
    want_list_table_dict["object_CID"] = "null"
    want_list_table_dict["insert_DTS"] = "null"
    want_list_table_dict["last_update_DTS"] = "null"
    want_list_table_dict["insert_update_delta"] = 0
    want_list_table_dict["source_peer_type"] = "null"
    return want_list_table_dict


def get_header_table_dict():
    header_table_dict = {}
    header_table_dict["version"] = "0"
    header_table_dict["object_CID"] = "null"
    header_table_dict["object_type"] = "null"
    header_table_dict["insert_DTS"] = "null"
    header_table_dict["prior_header_CID"] = "null"
    header_table_dict["header_CID"] = "null"
    return header_table_dict
