from diyims.beacon import beacon_main, satisfy_main
from diyims.queue_server import queue_main
from diyims.peer_capture import (
    capture_providers_main,
    capture_bitswap_main,
    capture_swarm_main,
)
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
def test_capture_providers():
    capture_providers_main()


@pytest.mark.mp
# @pytest.mark.xdist_group(name="group2")
def test_capture_bitswap():
    capture_bitswap_main()


@pytest.mark.mp
# @pytest.mark.xdist_group(name="group2")
def test_capture_swarm():
    capture_swarm_main()


@pytest.mark.mp
# @pytest.mark.xdist_group(name="group2")
def test_capture_want_lists():
    process_peers()
