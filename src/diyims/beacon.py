import requests
from time import sleep
from diyims.ipfs_utils import get_url_dict


def do_work(logger, beacon_CID):
    flash_beacon(logger, beacon_CID)

    return


def flash_beacon(logger, beacon_CID):
    url_dict = get_url_dict()
    get_arg = {
        "arg": beacon_CID,
        # "output": str(path_dict['log_path']) + '/' + IPNS_name + '.txt',  # NOTE: Path does not work
    }
    i = 0
    not_found = True
    while i < 30 and not_found:
        try:
            with requests.Session().post(
                url_dict["get"], params=get_arg, stream=False
            ) as r:
                r.raise_for_status()
                not_found = False
                logger.debug("Flash")
        except ConnectionError:
            logger.exception()
            sleep(1)
            i += 1
    return
