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

import requests

from diyims.urls import get_url_dict


def get_providers():
    url_dict = get_url_dict()

    key_arg = {"arg": "Qmbtf9BLMEhYZcmTL3pWpfF2RdTVVzrF42b31XGm6x2XLp"}

    with requests.post(url_dict["find_providers"], params=key_arg, stream=True) as r:
        count = 0
        for line in r.iter_lines():
            if line:
                count = count + 1
                decoded_line = line.decode("utf-8")
                json_dict = json.loads(decoded_line)
                if json_dict["Type"] == 4:
                    json_string = str(json_dict["Responses"])
                    json_string_len = len(json_string)
                    python_string = json_string[1 : json_string_len - 1]
                    python_dict = json.loads(python_string.replace("'", '"'))
                print(python_dict["ID"], json_dict["Type"])
        # print(count)
