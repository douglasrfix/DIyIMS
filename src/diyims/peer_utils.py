"""
NOTE: Contains FINDPROVS speculation.

It appears that the output of findprovs  returns an 'ID' value of null for 'Type' 4.
'Type' 4 is one of several records(?) in the routing system.

The ID can be found in 'Responses'

The content of 'Responses' is not JSON. You have to trim the brackets and replace single
quotes with double quotes. This was sufficient for my needs but YMMV.

This appears to yield the same results as the CLI

The routing system has some inertia and retains the node as a provider after the cid is
removed and a garbage collection has run.

"""

import json
import sqlite3
import configparser
import requests
from pathlib import Path
from diyims.ipfs_utils import get_url_dict
from diyims.path_utils import (
    get_path_dict,
    get_install_template_dict,
)

from diyims.error_classes import ApplicationNotInstalledError
from datetime import datetime, timezone
from sqlite3 import IntegrityError
from rich import print

from diyims.database_utils import insert_peer_row, refresh_peer_table_dict
from diyims.general_utils import get_network_name


def get_providers():
    url_dict = get_url_dict()
    path_dict = get_path_dict()
    network_name = get_network_name()
    connect_path = path_dict["db_file"]
    conn = sqlite3.connect(connect_path)
    key_arg = {"arg": network_name}
    with requests.post(url_dict["find_providers"], params=key_arg, stream=True) as r:
        r.raise_for_status()
        found = 0
        added = 0
        for line in r.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                json_dict = json.loads(decoded_line)
                if json_dict["Type"] == 4:
                    json_string = str(
                        json_dict["Responses"]
                    )  # NOTE: dictionary of lists?
                    json_string_len = len(json_string)
                    python_string = json_string[1 : json_string_len - 1]
                    python_dict = json.loads(python_string.replace("'", '"'))
                    # print(python_dict["ID"], json_dict["Type"])
                    # provider_dict[python_dict["ID"]] = python_dict["ID"]

                    peer_table_dict = refresh_peer_table_dict()
                    DTS = str(datetime.now(timezone.utc))
                    peer_table_dict["peer_ID"] = python_dict["ID"]
                    peer_table_dict["local_update_DTS"] = DTS
                    peer_table_dict["processing_status"] = "NP"
                    try:
                        insert_peer_row(conn, peer_table_dict)
                        conn.commit()
                        added = added + 1
                    except IntegrityError:
                        pass
                    found = found + 1
    conn.close()
    print(f"{found} providers found and {added} providers added")
    return


def get_peer_capture_dict():
    install_dict = get_install_template_dict()

    config_file = Path().joinpath(install_dict["config_path"], "diyims.ini")
    parser = configparser.ConfigParser()

    try:
        with open(config_file, "r") as configfile:
            parser.read_file(configfile)

    except FileNotFoundError:
        raise ApplicationNotInstalledError(" ")

    beacon_dict = {}
    beacon_dict["minutes_to_run"] = parser["Beacon"]["minutes_to_run"]
    beacon_dict["long_period_seconds"] = parser["Beacon"]["long_period_seconds"]
    beacon_dict["short_period_seconds"] = parser["Beacon"]["short_period_seconds"]
    beacon_dict["number_of_periods"] = parser["Beacon"]["number_of_periods"]

    return beacon_dict
