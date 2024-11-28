import configparser
import json
import requests
from time import sleep
from pathlib import Path
from diyims.ipfs_utils import get_url_dict
from diyims.error_classes import ApplicationNotInstalledError
from diyims.path_utils import (
    get_install_template_dict,
)


def config_install():
    get_beacon_config_dict()
    get_satisfy_config_dict()
    get_queue_config_dict()
    get_scheduler_config_dict()
    get_ipfs_config_dict()
    get_peer_capture_config_dict()
    get_logger_config_dict()
    get_want_list_config_dict()

    return


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
        beacon_config_dict["long_period_seconds"] = parser["Beacon"][
            "long_period_seconds"
        ]
        beacon_config_dict["short_period_seconds"] = parser["Beacon"][
            "short_period_seconds"
        ]
        beacon_config_dict["number_of_periods"] = parser["Beacon"]["number_of_periods"]
        beacon_config_dict["sql_timeout"] = parser["Beacon"]["sql_timeout"]
        beacon_config_dict["wait_before_startup"] = parser["Beacon"][
            "wait_before_startup"
        ]
        beacon_config_dict["shutdown_time"] = parser["Beacon"]["shutdown_time"]
        beacon_config_dict["log_file"] = parser["Beacon"]["log_file"]

        beacon_config_dict["connect_retries"] = parser["Beacon"]["connect_retries"]
        beacon_config_dict["connect_retry_delay"] = parser["Beacon"][
            "connect_retry_delay"
        ]
    except KeyError:
        parser["Beacon"] = {}
        parser["Beacon"]["long_period_seconds"] = "120"
        parser["Beacon"]["short_period_seconds"] = "60"
        parser["Beacon"]["number_of_periods"] = "5"
        parser["Beacon"]["sql_timeout"] = "60"
        parser["Beacon"]["wait_before_startup"] = "15"
        parser["Beacon"]["shutdown_time"] = "22:0:0"
        parser["Beacon"]["log_file"] = "beacon.log"
        parser["Beacon"]["connect_retries"] = "30"
        parser["Beacon"]["connect_retry_delay"] = "30"
        with open(config_file, "w") as configfile:
            parser.write(configfile)

        beacon_config_dict = {}
        beacon_config_dict["long_period_seconds"] = parser["Beacon"][
            "long_period_seconds"
        ]
        beacon_config_dict["short_period_seconds"] = parser["Beacon"][
            "short_period_seconds"
        ]
        beacon_config_dict["number_of_periods"] = parser["Beacon"]["number_of_periods"]
        beacon_config_dict["sql_timeout"] = parser["Beacon"]["sql_timeout"]
        beacon_config_dict["wait_before_startup"] = parser["Beacon"][
            "wait_before_startup"
        ]
        beacon_config_dict["shutdown_time"] = parser["Beacon"]["shutdown_time"]
        beacon_config_dict["log_file"] = parser["Beacon"]["log_file"]

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
        satisfy_config_dict["wait_before_startup"] = parser["Satisfy"][
            "wait_before_startup"
        ]
        satisfy_config_dict["log_file"] = parser["Satisfy"]["log_file"]
        satisfy_config_dict["connect_retries"] = parser["Satisfy"]["connect_retries"]
        satisfy_config_dict["connect_retry_delay"] = parser["Satisfy"][
            "connect_retry_delay"
        ]

    except KeyError:
        parser["Satisfy"] = {}
        parser["Satisfy"]["wait_before_startup"] = "30"
        parser["Satisfy"]["log_file"] = "satisfy.log"
        parser["Satisfy"]["connect_retries"] = "30"
        parser["Satisfy"]["connect_retry_delay"] = "30"
        with open(config_file, "w") as configfile:
            parser.write(configfile)

        satisfy_config_dict = {}
        satisfy_config_dict["wait_before_startup"] = parser["Satisfy"][
            "wait_before_startup"
        ]
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
        queue_config_dict["wait_before_startup"] = parser["Queue"][
            "wait_before_startup"
        ]
        queue_config_dict["log_file"] = parser["Queue"]["log_file"]

    except KeyError:
        parser["Queue"] = {}
        parser["Queue"]["wait_before_startup"] = "0"
        parser["Queue"]["log_file"] = "queue.log"

        with open(config_file, "w") as configfile:
            parser.write(configfile)

        queue_config_dict = {}
        queue_config_dict["wait_before_startup"] = parser["Queue"][
            "wait_before_startup"
        ]
        queue_config_dict["log_file"] = parser["Queue"]["log_file"]

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
        scheduler_config_dict["submit_delay"] = parser["Scheduler"]["submit_delay"]
        scheduler_config_dict["worker_pool"] = parser["Scheduler"]["worker_pool"]
        scheduler_config_dict["shutdown_delay"] = parser["Scheduler"]["shutdown_delay"]
        scheduler_config_dict["wait_before_startup"] = parser["Scheduler"][
            "wait_before_startup"
        ]
        scheduler_config_dict["log_file"] = parser["Scheduler"]["log_file"]

    except KeyError:
        parser["Scheduler"] = {}
        parser["Scheduler"]["submit_delay"] = "0"
        parser["Scheduler"]["worker_pool"] = "5"
        parser["Scheduler"]["shutdown_delay"] = "5"
        parser["Scheduler"]["wait_before_startup"] = "0"
        parser["Scheduler"]["log_file"] = "scheduler.log"

        with open(config_file, "w") as configfile:
            parser.write(configfile)

        scheduler_config_dict = {}
        scheduler_config_dict["submit_delay"] = parser["Scheduler"]["submit_delay"]
        scheduler_config_dict["worker_pool"] = parser["Scheduler"]["worker_pool"]
        scheduler_config_dict["shutdown_delay"] = parser["Scheduler"]["shutdown_delay"]
        scheduler_config_dict["wait_before_startup"] = parser["Scheduler"][
            "wait_before_startup"
        ]
        scheduler_config_dict["log_file"] = parser["Scheduler"]["log_file"]

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
        ipfs_config_dict["agent"] = parser["IPFS"]["agent"]
        ipfs_config_dict["connect_retries"] = parser["IPFS"]["connect_retries"]
        ipfs_config_dict["connect_retry_delay"] = parser["IPFS"]["connect_retry_delay"]

    except KeyError:
        url_dict = get_url_dict()
        i = 0
        not_found = True
        while i < 30 and not_found:
            try:
                with requests.post(url_dict["id"], stream=False) as r:
                    json_dict = json.loads(r.text)
                    not_found = False
            except ConnectionError:
                sleep(10)
                i += 1

        parser["IPFS"] = {}
        parser["IPFS"]["agent"] = json_dict["AgentVersion"]
        parser["IPFS"]["connect_retries"] = "30"
        parser["IPFS"]["connect_retry_delay"] = "30"

        with open(config_file, "w") as configfile:
            parser.write(configfile)

        ipfs_config_dict = {}
        ipfs_config_dict["agent"] = parser["IPFS"]["agent"]
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
        peer_capture_config_dict["capture_interval_delay"] = parser["Peer_Capture"][
            "capture_interval_delay"
        ]
        peer_capture_config_dict["sql_timeout"] = parser["Peer_Capture"]["sql_timeout"]
        peer_capture_config_dict["wait_before_startup"] = parser["Peer_Capture"][
            "wait_before_startup"
        ]
        peer_capture_config_dict["shutdown_time"] = parser["Peer_Capture"][
            "shutdown_time"
        ]
        peer_capture_config_dict["log_file"] = parser["Peer_Capture"]["log_file"]
        peer_capture_config_dict["connect_retries"] = parser["Peer_Capture"][
            "connect_retries"
        ]
        peer_capture_config_dict["connect_retry_delay"] = parser["Peer_Capture"][
            "connect_retry_delay"
        ]

    except KeyError:
        parser["Peer_Capture"] = {}
        parser["Peer_Capture"]["capture_interval_delay"] = "600"
        parser["Peer_Capture"]["sql_timeout"] = "60"
        parser["Peer_Capture"]["wait_before_startup"] = "0"
        parser["Peer_Capture"]["shutdown_time"] = "23:0:0"
        parser["Peer_Capture"]["log_file"] = "peer_capture.log"
        parser["Peer_Capture"]["connect_retries"] = "30"
        parser["Peer_Capture"]["connect_retry_delay"] = "30"

        with open(config_file, "w") as configfile:
            parser.write(configfile)

        peer_capture_config_dict = {}
        peer_capture_config_dict["capture_interval_delay"] = parser["Peer_Capture"][
            "capture_interval_delay"
        ]
        peer_capture_config_dict["sql_timeout"] = parser["Peer_Capture"]["sql_timeout"]
        peer_capture_config_dict["wait_before_startup"] = parser["Peer_Capture"][
            "wait_before_startup"
        ]
        peer_capture_config_dict["shutdown_time"] = parser["Peer_Capture"][
            "shutdown_time"
        ]
        peer_capture_config_dict["log_file"] = parser["Peer_Capture"]["log_file"]
        peer_capture_config_dict["connect_retries"] = parser["Peer_Capture"][
            "connect_retries"
        ]
        peer_capture_config_dict["connect_retry_delay"] = parser["Peer_Capture"][
            "connect_retry_delay"
        ]

    return peer_capture_config_dict


def get_logger_config_dict():
    install_dict = get_install_template_dict()

    config_file = Path().joinpath(install_dict["config_path"], "diyims.ini")
    parser = configparser.ConfigParser()

    try:
        with open(config_file, "r") as configfile:
            parser.read_file(configfile)

    except FileNotFoundError:
        raise ApplicationNotInstalledError(" ")

    try:
        logger_config_dict = {}
        logger_config_dict["default_level"] = parser["Logger"]["default_level"]
        logger_config_dict["console_level"] = parser["Logger"]["console_level"]
        logger_config_dict["file_level"] = parser["Logger"]["file_level"]

    except KeyError:
        parser["Logger"] = {}
        parser["Logger"]["default_level"] = "DEBUG"
        parser["Logger"]["console_level"] = "INFO"
        parser["Logger"]["file_level"] = "DEBUG"

        with open(config_file, "w") as configfile:
            parser.write(configfile)

        logger_config_dict = {}
        logger_config_dict["default_level"] = parser["Logger"]["default_level"]
        logger_config_dict["console_level"] = parser["Logger"]["console_level"]
        logger_config_dict["file_level"] = parser["Logger"]["file_level"]

    return logger_config_dict


def get_want_list_config_dict():
    install_dict = get_install_template_dict()

    config_file = Path().joinpath(install_dict["config_path"], "diyims.ini")
    parser = configparser.ConfigParser()

    try:
        with open(config_file, "r") as configfile:
            parser.read_file(configfile)

    except FileNotFoundError:
        raise ApplicationNotInstalledError(" ")

    try:
        want_list_config_dict = {}
        want_list_config_dict["samples_per_minute"] = parser["Want_List"][
            "samples_per_minute"
        ]
        want_list_config_dict["number_of_samples"] = parser["Want_List"][
            "number_of_samples"
        ]
        want_list_config_dict["sql_timeout"] = parser["Want_List"]["sql_timeout"]
        want_list_config_dict["wait_before_startup"] = parser["Want_List"][
            "wait_before_startup"
        ]
        want_list_config_dict["shutdown_time"] = parser["Want_List"]["shutdown_time"]
        want_list_config_dict["log_file"] = parser["Want_List"]["log_file"]
        want_list_config_dict["connect_retries"] = parser["Want_List"][
            "connect_retries"
        ]
        want_list_config_dict["connect_retry_delay"] = parser["Want_List"][
            "connect_retry_delay"
        ]

    except KeyError:
        parser["Want_List"] = {}
        parser["Want_List"]["samples_per_minute"] = "6"
        parser["Want_List"]["number_of_samples"] = "10"
        parser["Want_List"]["sql_timeout"] = "60"
        parser["Want_List"]["wait_before_startup"] = "0"
        parser["Want_List"]["shutdown_time"] = "23:0:0"
        parser["Want_List"]["log_file"] = "want_list.log"
        parser["Want_List"]["connect_retries"] = "30"
        parser["Want_List"]["connect_retry_delay"] = "30"

        with open(config_file, "w") as configfile:
            parser.write(configfile)

        want_list_config_dict = {}
        want_list_config_dict["samples_per_minute"] = parser["Want_List"][
            "samples_per_minute"
        ]
        want_list_config_dict["number_of_samples"] = parser["Want_List"][
            "number_of_samples"
        ]
        want_list_config_dict["sql_timeout"] = parser["Want_List"]["sql_timeout"]
        want_list_config_dict["wait_before_startup"] = parser["Want_List"][
            "wait_before_startup"
        ]
        want_list_config_dict["shutdown_time"] = parser["Want_List"]["shutdown_time"]
        want_list_config_dict["log_file"] = parser["Want_List"]["log_file"]
        want_list_config_dict["connect_retries"] = parser["Want_List"][
            "connect_retries"
        ]
        want_list_config_dict["connect_retry_delay"] = parser["Want_List"][
            "connect_retry_delay"
        ]

    return want_list_config_dict
