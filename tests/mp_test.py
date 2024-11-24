from diyims.beacon import beacon_main
from diyims.satisfy import satisfy_main
from diyims.queue_server import queue_main
from time import sleep
import pytest


@pytest.mark.mp
# @pytest.mark.xdist_group(name="group1")
def test_mss():
    queue_main()


# @pytest.mark.skip(reason="native")
# @pytest.mark.run
@pytest.mark.mp
# @pytest.mark.xdist_group(name="group1")
def test_mp1():
    sleep(15)
    beacon_main()


@pytest.mark.mp
# @pytest.mark.xdist_group(name="group2")
def test_mp2():
    sleep(15)
    satisfy_main()
