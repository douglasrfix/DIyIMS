import configparser
from pathlib import Path
from diyims.error_classes import ApplicationNotInstalledError
from diyims.path_utils import (
    get_install_template_dict,
)


def get_beacon_config_dict():
    install_dict = get_install_template_dict()

    config_file = Path().joinpath(install_dict["config_path"], "diyims.ini")
    parser = configparser.ConfigParser()

    try:
        with open(config_file, "r") as configfile:
            parser.read_file(configfile)

    except FileNotFoundError:
        raise ApplicationNotInstalledError(" ")

    try:
        beacon_config_dict = {}
        beacon_config_dict["shutdown_offset_hours"] = parser["Beacon"][
            "shutdown_offset_hours"
        ]
        beacon_config_dict["long_period_seconds"] = parser["Beacon"][
            "long_period_seconds"
        ]
        beacon_config_dict["short_period_seconds"] = parser["Beacon"][
            "short_period_seconds"
        ]
        beacon_config_dict["number_of_periods"] = parser["Beacon"]["number_of_periods"]
        beacon_config_dict["log_file"] = parser["Beacon"]["log_file"]
        beacon_config_dict["sql_timeout"] = parser["Beacon"]["sql_timeout"]
        beacon_config_dict["connect_retries"] = parser["Beacon"]["connect_retries"]
        beacon_config_dict["connect_retry_delay"] = parser["Beacon"][
            "connect_retry_delay"
        ]
    except KeyError:
        parser["Beacon"] = {}
        parser["Beacon"]["shutdown_offset_hours"] = "1"
        parser["Beacon"]["long_period_seconds"] = "120"
        parser["Beacon"]["short_period_seconds"] = "60"
        parser["Beacon"]["number_of_periods"] = "5"
        parser["Beacon"]["log_file"] = "beacon.log"
        parser["Beacon"]["sql_timeout"] = "60"
        parser["Beacon"]["connect_retries"] = "30"
        parser["Beacon"]["connect_retry_delay"] = "30"
        with open(config_file, "w") as configfile:
            parser.write(configfile)

        beacon_config_dict = {}
        beacon_config_dict["shutdown_offset_hours"] = parser["Beacon"][
            "shutdown_offset_hours"
        ]
        beacon_config_dict["long_period_seconds"] = parser["Beacon"][
            "long_period_seconds"
        ]
        beacon_config_dict["short_period_seconds"] = parser["Beacon"][
            "short_period_seconds"
        ]
        beacon_config_dict["number_of_periods"] = parser["Beacon"]["number_of_periods"]
        beacon_config_dict["log_file"] = parser["Beacon"]["log_file"]
        beacon_config_dict["sql_timeout"] = parser["Beacon"]["sql_timeout"]
        beacon_config_dict["connect_retries"] = parser["Beacon"]["connect_retries"]
        beacon_config_dict["connect_retry_delay"] = parser["Beacon"][
            "connect_retry_delay"
        ]

    return beacon_config_dict


def get_satisfy_config_dict():
    install_dict = get_install_template_dict()

    config_file = Path().joinpath(install_dict["config_path"], "diyims.ini")
    parser = configparser.ConfigParser()

    try:
        with open(config_file, "r") as configfile:
            parser.read_file(configfile)

    except FileNotFoundError:
        raise ApplicationNotInstalledError(" ")

    try:
        satisfy_config_dict = {}
        satisfy_config_dict["log_file"] = parser["Satisfy"]["log_file"]
        satisfy_config_dict["connect_retries"] = parser["Satisfy"]["connect_retries"]
        satisfy_config_dict["connect_retry_delay"] = parser["Satisfy"][
            "connect_retry_delay"
        ]

    except KeyError:
        parser["Satisfy"] = {}
        parser["Satisfy"]["log_file"] = "satisfy.log"
        parser["Satisfy"]["connect_retries"] = "30"
        parser["Satisfy"]["connect_retry_delay"] = "30"
        with open(config_file, "w") as configfile:
            parser.write(configfile)

        satisfy_config_dict = {}
        satisfy_config_dict["log_file"] = parser["Satisfy"]["log_file"]
        satisfy_config_dict["connect_retries"] = parser["Satisfy"]["connect_retries"]
        satisfy_config_dict["connect_retry_delay"] = parser["Satisfy"][
            "connect_retry_delay"
        ]

    return satisfy_config_dict


def get_queue_config_dict():
    install_dict = get_install_template_dict()

    config_file = Path().joinpath(install_dict["config_path"], "diyims.ini")
    parser = configparser.ConfigParser()

    try:
        with open(config_file, "r") as configfile:
            parser.read_file(configfile)

    except FileNotFoundError:
        raise ApplicationNotInstalledError(" ")

    try:
        queue_config_dict = {}
        queue_config_dict["shutdown_offset_hours"] = parser["Queue"][
            "shutdown_offset_hours"
        ]
        queue_config_dict["log_file"] = parser["Queue"]["log_file"]
        queue_config_dict["midnight_loop_delay"] = parser["Queue"][
            "midnight_loop_delay"
        ]

    except KeyError:
        parser["Queue"] = {}
        parser["Queue"]["shutdown_offset_hours"] = "1"
        parser["Queue"]["log_file"] = "queue.log"
        parser["Queue"]["midnight_loop_delay"] = "60"
        with open(config_file, "w") as configfile:
            parser.write(configfile)

        queue_config_dict = {}
        queue_config_dict["shutdown_offset_hours"] = parser["Queue"][
            "shutdown_offset_hours"
        ]
        queue_config_dict["log_file"] = parser["Queue"]["log_file"]
        queue_config_dict["midnight_loop_delay"] = parser["Queue"][
            "Midnight_loop_delay"
        ]

    return queue_config_dict


def get_scheduler_config_dict():
    install_dict = get_install_template_dict()

    config_file = Path().joinpath(install_dict["config_path"], "diyims.ini")
    parser = configparser.ConfigParser()

    try:
        with open(config_file, "r") as configfile:
            parser.read_file(configfile)

    except FileNotFoundError:
        raise ApplicationNotInstalledError(" ")

    try:
        scheduler_config_dict = {}
        scheduler_config_dict["log_file"] = parser["Scheduler"]["log_file"]
        scheduler_config_dict["submit_delay"] = parser["Scheduler"]["submit_delay"]
        scheduler_config_dict["worker_pool"] = parser["Scheduler"]["worker_pool"]

    except KeyError:
        parser["Scheduler"] = {}
        parser["Scheduler"]["log_file"] = "scheduler.log"
        parser["Scheduler"]["submit_delay"] = "30"
        parser["Scheduler"]["worker_pool"] = "5"

        with open(config_file, "w") as configfile:
            parser.write(configfile)

        scheduler_config_dict = {}
        scheduler_config_dict["log_file"] = parser["Scheduler"]["log_file"]
        scheduler_config_dict["submit_delay"] = parser["Scheduler"]["submit_delay"]
        scheduler_config_dict["worker_pool"] = parser["Scheduler"]["worker_pool"]

    return scheduler_config_dict


def get_ipfs_config_dict():
    install_dict = get_install_template_dict()

    config_file = Path().joinpath(install_dict["config_path"], "diyims.ini")
    parser = configparser.ConfigParser()

    try:
        with open(config_file, "r") as configfile:
            parser.read_file(configfile)

    except FileNotFoundError:
        raise ApplicationNotInstalledError(" ")

    try:
        ipfs_config_dict = {}
        ipfs_config_dict["connect_retries"] = parser["IPFS"]["connect_retries"]
        ipfs_config_dict["connect_retry_delay"] = parser["IPFS"]["connect_retry_delay"]

    except KeyError:
        # parser["IPFS"] = {}
        parser["IPFS"]["connect_retries"] = "30"
        parser["IPFS"]["connect_retry_delay"] = "30"

        with open(config_file, "w") as configfile:
            parser.write(configfile)

        ipfs_config_dict = {}
        ipfs_config_dict["connect_retries"] = parser["IPFS"]["connect_retries"]
        ipfs_config_dict["connect_retry_delay"] = parser["IPFS"]["connect_retry_delay"]

    return ipfs_config_dict


def get_peer_capture_config_dict():
    install_dict = get_install_template_dict()

    config_file = Path().joinpath(install_dict["config_path"], "diyims.ini")
    parser = configparser.ConfigParser()

    try:
        with open(config_file, "r") as configfile:
            parser.read_file(configfile)

    except FileNotFoundError:
        raise ApplicationNotInstalledError(" ")

    try:
        peer_capture_config_dict = {}
        peer_capture_config_dict["shutdown_offset_hours"] = parser["Peer_Capture"][
            "shutdown_offset_hours"
        ]
        peer_capture_config_dict["log_file"] = parser["Peer_Capture"]["log_file"]
        peer_capture_config_dict["check_interval_delay"] = parser["Peer_Capture"][
            "check_interval_delay"
        ]

    except KeyError:
        parser["Peer_Capture"] = {}
        parser["Peer_Capture"]["shutdown_offset_hours"] = "1"
        parser["Peer_Capture"]["log_file"] = "queue.log"
        parser["Peer_Capture"]["check_interval_delay"] = "600"
        with open(config_file, "w") as configfile:
            parser.write(configfile)

        peer_capture_config_dict = {}
        peer_capture_config_dict["shutdown_offset_hours"] = parser["Peer_Capture"][
            "shutdown_offset_hours"
        ]
        peer_capture_config_dict["log_file"] = parser["Peer_Capture"]["log_file"]
        peer_capture_config_dict["check_interval_delay"] = parser["Peer_Capture"][
            "check_interval_delay"
        ]

    return peer_capture_config_dict
