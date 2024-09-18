import json

import requests

from diyims.urls import get_url_dict


def test():
    url_dict = get_url_dict()
    with requests.post(url_dict["pin_list"], stream=False) as r:
        r.raise_for_status()
        json_dict = json.loads(r.text)

        try:
            for key in json_dict["Keys"]:
                add_params = {"arg": key}

                with requests.post(
                    url_dict["pin_remove"], params=add_params, stream=False
                ) as r:
                    r.raise_for_status()

        except KeyError:
            pass

    with requests.post(url_dict["run_gc"], stream=False) as r:
        r.raise_for_status()
