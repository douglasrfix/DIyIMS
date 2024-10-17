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
from datetime import datetime, timezone
from sqlite3 import IntegrityError

import requests

from diyims.general_utils import get_network_name
from diyims.database_operations import insert_peer_row
from diyims.sql_table_dict import refresh_peer_table_dict
from diyims.url_utils import get_url_dict


def get_providers():
    url_dict = get_url_dict()
    network_name = get_network_name()
    key_arg = {"arg": network_name}
    # provider_dict = {}

    with requests.post(url_dict["find_providers"], params=key_arg, stream=True) as r:
        r.raise_for_status()
        count = 0
        for line in r.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                json_dict = json.loads(decoded_line)
                if json_dict["Type"] == 4:
                    json_string = str(json_dict["Responses"])
                    json_string_len = len(json_string)
                    python_string = json_string[1 : json_string_len - 1]
                    python_dict = json.loads(python_string.replace("'", '"'))
                    # print(python_dict["ID"], json_dict["Type"])
                    # provider_dict[python_dict["ID"]] = python_dict["ID"]

                    peer_table_dict = refresh_peer_table_dict()
                    DTS = str(datetime.now(timezone.utc))
                    peer_table_dict["peer_ID"] = python_dict["ID"]
                    peer_table_dict["local_update_DTS"] = DTS
                    peer_table_dict["processing_status"] = "A"
                    try:
                        insert_peer_row(peer_table_dict)
                        count = count + 1
                    except IntegrityError:
                        pass
        print(count)
        # print(provider_dict)
