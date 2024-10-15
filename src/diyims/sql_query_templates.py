"""
queries.insert_peer_row(
    conn,
    peer_table_dict["version"],
    peer_table_dict["peer_id"],
    peer_table_dict["update_seq"],
    peer_table_dict["IPNS_name"],
    peer_table_dict["update_dts"],
    peer_table_dict["platform"],
    peer_table_dict["python_version"],
    peer_table_dict["ipfs_agent"],
)

queries.insert_network_row(
    conn,
    network_table_dict["version"],
    network_table_dict["network_name"],
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
