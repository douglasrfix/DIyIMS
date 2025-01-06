def set_up_sql_operations(config_dict):
    from diyims.path_utils import get_path_dict
    from diyims.py_version_dep import get_sql_str
    import aiosql
    import sqlite3

    path_dict = get_path_dict()
    sql_str = get_sql_str()
    connect_path = path_dict["db_file"]
    queries = aiosql.from_str(sql_str, "sqlite3")
    conn = sqlite3.connect(connect_path, timeout=int(config_dict["sql_timeout"]))
    conn.row_factory = sqlite3.Row
    return conn, queries


def reset_peer_table_status():
    from diyims.config_utils import get_want_list_config_dict
    from diyims.path_utils import get_path_dict
    from diyims.py_version_dep import get_sql_str
    import aiosql
    import sqlite3

    config_dict = get_want_list_config_dict()
    path_dict = get_path_dict()
    sql_str = get_sql_str()
    connect_path = path_dict["db_file"]
    queries = aiosql.from_str(sql_str, "sqlite3")
    conn = sqlite3.connect(connect_path, timeout=int(config_dict["sql_timeout"]))
    conn.row_factory = sqlite3.Row

    queries.reset_peer_table_status(
        conn,
    )
    conn.commit()
    conn.close()
    return


def insert_peer_row(conn, queries, peer_table_dict):
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


def select_peer_table_entry_by_key(conn, queries, peer_table_dict):
    peer_table_entry = queries.select_peer_table_entry_by_key(
        conn,
        peer_table_dict["peer_ID"],
    )
    return peer_table_entry


def update_peer_table_peer_type_status(conn, queries, peer_table_dict):
    queries.update_peer_table_peer_type_status(
        conn,
        peer_table_dict["peer_type"],
        peer_table_dict["processing_status"],
        peer_table_dict["local_update_DTS"],
        peer_table_dict["peer_ID"],
    )
    return


def update_peer_table_status_WLR(conn, queries, peer_table_dict):
    queries.update_peer_table_status_WLR(
        conn,
        peer_table_dict["processing_status"],
        peer_table_dict["local_update_DTS"],
        peer_table_dict["peer_ID"],
    )
    return


def update_peer_table_status_WLP(conn, queries, peer_table_dict):
    queries.update_peer_table_status_WLP(
        conn,
        peer_table_dict["processing_status"],
        peer_table_dict["local_update_DTS"],
        peer_table_dict["peer_ID"],
    )
    return


def update_peer_table_status_WLX(conn, queries, peer_table_dict):
    queries.update_peer_table_status_WLX(
        conn,
        peer_table_dict["processing_status"],
        peer_table_dict["local_update_DTS"],
        peer_table_dict["peer_ID"],
    )
    return


def update_peer_table_status_WLZ(conn, queries, peer_table_dict):
    queries.update_peer_table_status_WLZ(
        conn,
        peer_table_dict["processing_status"],
        peer_table_dict["local_update_DTS"],
        peer_table_dict["peer_ID"],
    )
    return


def update_peer_table_IPNS_name_status_NPC(conn, queries, peer_table_dict):
    queries.update_peer_table_IPNS_name_status_NPC(
        conn,
        peer_table_dict["IPNS_name"],
        peer_table_dict["processing_status"],
        peer_table_dict["local_update_DTS"],
        peer_table_dict["peer_ID"],
    )
    return


def refresh_peer_table_dict():
    peer_table_dict = {}
    peer_table_dict["peer_ID"] = "null"
    peer_table_dict["IPNS_name"] = "null"
    peer_table_dict["peer_type"] = "null"
    peer_table_dict["origin_update_DTS"] = "null"
    peer_table_dict["local_update_DTS"] = "null"
    peer_table_dict["wanted_found"] = "0"
    peer_table_dict["wanted_added"] = "0"
    peer_table_dict["wanted_updated"] = "0"
    peer_table_dict["zero_cid_samples"] = "0"
    peer_table_dict["connection_retry_iteration"] = "null"
    peer_table_dict["execution_platform"] = "null"
    peer_table_dict["python_version"] = "null"
    peer_table_dict["IPFS_agent"] = "null"
    peer_table_dict["processing_status"] = "null"
    peer_table_dict["agent"] = "null"
    peer_table_dict["version"] = "0"

    return peer_table_dict


def insert_network_row(conn, queries, network_table_dict):
    queries.insert_network_row(
        conn,
        network_table_dict["network_name"],
    )
    return


def select_network_name(conn, queries, network_table_dict):
    network_table_dict = queries.select_network_name(
        conn,
    )
    return network_table_dict


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


if __name__ == "__main__":
    reset_peer_table_status()
