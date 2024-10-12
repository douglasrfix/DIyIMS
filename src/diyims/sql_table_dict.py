def get_network_table_dict():
    network_table_dict = {}
    network_table_dict["version"] = "0"
    network_table_dict["network_name"] = "null"
    return network_table_dict


def get_peer_table_dict():
    peer_table_dict = {}
    peer_table_dict["version"] = "0"
    peer_table_dict["peer_id"] = "null"
    peer_table_dict["update_seq"] = 0
    peer_table_dict["IPNS_name"] = "null"
    peer_table_dict["update_dts"] = "null"
    peer_table_dict["platform"] = "null"
    peer_table_dict["python_version"] = "null"
    peer_table_dict["ipfs_agent"] = "null"
    return peer_table_dict
