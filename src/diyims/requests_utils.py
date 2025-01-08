from time import sleep
import requests
from requests.exceptions import ConnectionError, HTTPError


def execute_request(url_key, **kwargs):
    try:
        url_dict = kwargs["url_dict"]
    except KeyError:
        url_dict = ""
    try:
        config_dict = kwargs["config_dict"]
    except KeyError:
        config_dict = ""
    try:
        param = kwargs["param"]
    except KeyError:
        param = ""
    try:
        file = kwargs["file"]
    except KeyError:
        file = ""
    try:
        logger = kwargs["logger"]
    except KeyError:
        logger = ""

    if config_dict:
        connect_retries = int(config_dict["connect_retries"])
        connect_retry_delay = int(config_dict["connect_retry_delay"])
    else:
        connect_retries = 30
        connect_retry_delay = 10

    retry = 0
    response_ok = False
    while retry < connect_retries and not response_ok:
        try:
            if file:
                with requests.post(
                    url_dict[url_key],
                    params=param,
                    files=file,
                    stream=False,
                ) as r:
                    r.raise_for_status()
                    response_ok = True
            else:
                with requests.post(
                    url=url_dict[url_key],
                    params=param,
                    stream=False,
                ) as r:
                    r.raise_for_status()
                    response_ok = True
        except HTTPError:
            if logger:
                logger.exception(param)
        except ConnectionError:
            if logger:
                logger.exception()
            sleep(connect_retry_delay)
            retry += 1
    return r
