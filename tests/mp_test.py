from diyims.beacon import beacon_main, satisfy_main
from diyims.queue_server import queue_main
from diyims.peer_capture import peer_capture_main
from diyims.capture_want_lists import process_peers
import pytest


# @pytest.mark.skip
# @pytest.mark.xdist_group(name="group1")
def test_queue():
    queue_main()


# @pytest.mark.skip(reason="native")
# @pytest.mark.run
@pytest.mark.mp
# @pytest.mark.xdist_group(name="group1")
def test_beacon():
    beacon_main()


@pytest.mark.mp
# @pytest.mark.xdist_group(name="group2")
def test_satisfy():
    satisfy_main()


@pytest.mark.mp
# @pytest.mark.xdist_group(name="group2")
def test_peer_capture():
    peer_capture_main()


@pytest.mark.mp
# @pytest.mark.xdist_group(name="group2")
def test_capture_want_lists():
    process_peers()
