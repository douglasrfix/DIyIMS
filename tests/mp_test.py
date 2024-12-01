from diyims.beacon import beacon_main, satisfy_main
from diyims.peer_capture import (
    capture_providers_main,
    capture_bitswap_main,
    capture_swarm_main,
)
import pytest


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
