from time import sleep
import requests
from requests.exceptions import ConnectionError, HTTPError


def execute_request(logger, url_dict, url_key, config_dict, param, file):
    i = 0
    not_found = True
    while i < int(config_dict["connect_retries"]) and not_found:
        try:
            if file == "none":
                with requests.post(url_dict[url_key], params=param, stream=False) as r:
                    r.raise_for_status()
                    not_found = False
            else:
                with requests.post(
                    url=url_dict[url_key],
                    params=param,
                    files=file,
                ) as r:
                    r.raise_for_status()
                    not_found = False
        except HTTPError:
            if logger != "none":
                logger.exception(param)
        except ConnectionError:
            if logger != "none":
                logger.exception()
            sleep(int(config_dict["connect_retry_delay"]))
            i += 1
    return r
