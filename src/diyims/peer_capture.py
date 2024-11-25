from dateutil.relativedelta import relativedelta
from datetime import datetime
from time import sleep
from diyims.peer_utils import capture_providers
from diyims.logger_utils import get_logger
from diyims.config_utils import get_peer_capture_config_dict


def peer_capture_main():
    peer_capture_config_dict = get_peer_capture_config_dict()
    logger = get_logger(peer_capture_config_dict["log_file"])
    logger.info("Startup of Peer Capture.")

    current_DT = datetime.now()
    current_date = current_DT.date()
    mid_night = relativedelta(hour=23, minute=59, second=59)
    before_midnight = relativedelta(
        hours=+int(peer_capture_config_dict["shutdown_offset_hours"])
    )
    current_DT = datetime.now()
    target_DT = current_date + mid_night - before_midnight

    logger.info(f"Shutdown target {target_DT}")

    while target_DT > current_DT:
        capture_providers(logger)
        sleep(int(peer_capture_config_dict["check_interval_delay"]))
        current_DT = datetime.now()

    logger.info("Normal shutdown of Peer Capture.")
    return


if __name__ == "__main__":
    peer_capture_main()
