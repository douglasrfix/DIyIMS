from diyims.beacon import main as main1
from diyims.satisfy import main as main2
from diyims.queue_server import main
from time import sleep
import pytest


@pytest.mark.mp
# @pytest.mark.xdist_group(name="group1")
def test_mss():
    main()


# @pytest.mark.skip(reason="native")
# @pytest.mark.run
@pytest.mark.mp
# @pytest.mark.xdist_group(name="group1")
def test_mp1():
    sleep(15)
    main1()


@pytest.mark.mp
# @pytest.mark.xdist_group(name="group2")
def test_mp2():
    sleep(15)
    main2()
