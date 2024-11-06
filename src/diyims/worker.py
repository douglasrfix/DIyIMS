import requests
from diyims.ipfs_utils import get_url_dict


def do_work(beacon_CID):
    flash_beacon(beacon_CID)

    return  # result


def flash_beacon(beacon_CID):
    url_dict = get_url_dict()
    get_arg = {
        "arg": beacon_CID,
        # "output": str(path_dict['log_path']) + '/' + IPNS_name + '.txt',  # NOTE: Path does not work
    }

    with requests.post(url_dict["get"], params=get_arg, stream=False) as r:
        r.raise_for_status()

    return
