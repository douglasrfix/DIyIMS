"""
queries.insert_peer_row(
    conn,
    peer_table_dict["peer_id"],
    peer_table_dict["IPNS_name"],
    peer_table_dict["origin_update_DTS"],
    peer_table_dict["local_update_DTS"],
    peer_table_dict["execution_platform"],
    peer_table_dict["python_version"],
    peer_table_dict["IPFS_agent"],
    peer_table_dict["agent"],
    peer_table_dict["version"],
)

queries.insert_network_row(
    conn,
    network_table_dict["network_name"],
)

queries.insert_want_list_row(
    conn,
    want_list_table_dict["peer_ID"],
    want_list_table_dict["object_CID"],
)

queries.insert_header_row(
    conn,
    header_table_dict["version"],
    header_table_dict["object_CID"],
    header_table_dict["object_type"],
    header_table_dict["insert_DTS"],
    header_table_dict["prior_header_CID"],
    header_table_dict["header_CID"],
)

"""
