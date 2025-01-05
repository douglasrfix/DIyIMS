from datetime import datetime, timedelta, timezone

# from pathlib import Path
from rich import print
import json
from diyims.config_utils import get_want_list_config_dict

# from diyims.path_utils import get_path_dict
from diyims.ipfs_utils import get_url_dict
from diyims.database_utils import (
    set_up_sql_operations,
)
from diyims.requests_utils import execute_request


def filter_wantlist():
    want_list_config_dict = get_want_list_config_dict()
    # path_dict = get_path_dict()

    conn, queries = set_up_sql_operations(want_list_config_dict)

    current_DT = datetime.now(timezone.utc)
    off_set = timedelta(hours=15)
    duration = timedelta(hours=1)
    start_dts = current_DT - off_set
    end_dts = start_dts + duration
    query_start_dts = datetime.isoformat(start_dts)
    query_stop_dts = datetime.isoformat(end_dts)

    print(query_start_dts)
    print(query_stop_dts)
    rows_of_wantlist_items = queries.select_filter_want_list_by_start_stop(
        conn,
        query_start_dts,
        query_stop_dts,
    )
    for want_list_item in rows_of_wantlist_items:
        # print(want_list_item["object_CID"])
        # IPNS_name = want_list_item["object_CID"]
        # back_slash = "\\"
        # dot_txt = ".txt"
        # out_path = str(path_dict['log_path']) + back_slash + IPNS_name + dot_txt
        # out_file = open(out_path, 'wb')
        # print(out_path)
        url_dict = get_url_dict()
        param = {
            "arg": want_list_item["object_CID"],
        }
        url_key = "get"
        config_dict = want_list_config_dict
        file = "none"
        response = execute_request(
            "none",
            url_dict,
            url_key,
            config_dict,
            param,
            file,
        )

        start = response.text.find("{")
        end = response.text.find("}", start)
        end += 1
        string = response.text[start:end]
        print(string)
        json_dict = json.loads(string)

        print(json_dict["IPNS_name"])

        param = {
            "arg": json_dict["IPNS_name"],
        }
        url_key = "get"
        config_dict = want_list_config_dict
        file = "none"
        response = execute_request(
            "none",
            url_dict,
            url_key,
            config_dict,
            param,
            file,
        )

        start = response.text.find("{")
        end = response.text.find("}", start)
        end += 1
        string = response.text[start:end]
        print(string)
        json_dict = json.loads(string)

        print(json_dict)

        break

    # conn.close()


if __name__ == "__main__":
    filter_wantlist()
