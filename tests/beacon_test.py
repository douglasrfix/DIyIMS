import shlex

import pytest
from typer.testing import CliRunner

from diyims.diyims_cmd import app

runner = CliRunner()


# @pytest.mark.skip
def test_full_beacon():
    """testing find_providers with native windows install"""
    command_string = "beacon-utils beacon-operation"
    result = runner.invoke(app, shlex.split(command_string))
    print(result.stdout.rstrip())
    assert result.exit_code == 0


@pytest.mark.skip
def test_partial_beacon():
    """testing find_providers with native windows install"""
    command_string = "beacon-utils partial-beacon"
    result = runner.invoke(app, shlex.split(command_string))
    print(result.stdout.rstrip())
    assert result.exit_code == 0


# @pytest.mark.skip
def test_purge_beacon_items():
    """testing find_providers with native windows install"""
    command_string = "beacon-utils purge-beacon-files"
    result = runner.invoke(app, shlex.split(command_string))
    print(result.stdout.rstrip())
    assert result.exit_code == 0
