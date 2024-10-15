import json

import requests

"""
net work table layout

    node id
    self indicator
    ipns of the net work table
    cid of most recent notification table entry


Notification table

    cid of prior notification entry
    DTS of entry (UTC)
    cid of new object entry
    object type the new object entry points to

"""


"""
object types
    personal profile
    node profile ?
    object meta data
    document
    peer_table

"""

"""
url_dict = {}
url_dict['find_providers'] = 'http://127.0.0.1:5001/api/v0/routing/findprovs'
key_arg = {'arg': 'Qmbtf9BLMEhYZcmTL3pWpfF2RdTVVzrF42b31XGm6x2XLp'}



with requests.post(url_dict['find_providers'], params = key_arg, stream = True) as r:

    count = 0
    for line in r.iter_lines():
        if line:
            count = count + 1
            decoded_line = line.decode('utf-8')
            json_dict = json.loads(decoded_line)
            if json_dict['Type'] == 4:
                json_string = str(json_dict['Responses'])
                json_string_len = len(json_string)
                python_string = json_string[1:json_string_len - 1]
                python_dict = json.loads(python_string.replace("'", "\""))
                print(python_dict['ID'], json_dict['Type'])
    #print(count)

"""

url_dict = {}

url_dict["id"] = "http://127.0.0.1:5001/api/v0/id"

with requests.post(url_dict["id"], stream=False) as r:
    json_dict = json.loads(r.text)
    print(json_dict["ID"])
