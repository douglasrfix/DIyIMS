def refresh_network_table_dict():
    network_table_dict = {}
    network_table_dict["version"] = "0"
    network_table_dict["network_name"] = "null"
    return network_table_dict


def refresh_peer_table_dict():
    peer_table_dict = {}
    peer_table_dict["peer_ID"] = "null"
    peer_table_dict["IPNS_name"] = "null"
    peer_table_dict["origin_update_DTS"] = "null"
    peer_table_dict["local_update_DTS"] = "null"
    peer_table_dict["execution_platform"] = "null"
    peer_table_dict["python_version"] = "null"
    peer_table_dict["IPFS_agent"] = "null"
    peer_table_dict["processing_status"] = "null"
    peer_table_dict["version"] = "0"
    peer_table_dict["agent"] = "diyims/0.0.0"
    return peer_table_dict


def get_header_table_dict():
    header_table_dict = {}
    header_table_dict["version"] = "0"
    header_table_dict["object_CID"] = "null"
    header_table_dict["object_type"] = "null"
    header_table_dict["insert_DTS"] = "null"
    header_table_dict["prior_header_CID"] = "null"
    header_table_dict["header_CID"] = "null"
    return header_table_dict
