import shlex

import pytest
from typer.testing import CliRunner

from diyims.diyims import app

runner = CliRunner()


@pytest.mark.component
def test_find_providers():
    """testing find_providers with native windows install"""
    command_string = "find-providers"
    result = runner.invoke(app, shlex.split(command_string))
    print(result.stdout.rstrip())
    assert result.exit_code == 0


@pytest.mark.component
def test_capture_want_lists():
    """testing find_providers with native windows install"""
    command_string = "capture-want-lists --ten-second-intervals=1"
    result = runner.invoke(app, shlex.split(command_string))
    print(result.stdout.rstrip())
    assert result.exit_code == 0


@pytest.mark.component
def test_want_item_wait():
    """testing find_providers with native windows install"""
    command_string = "wait-on-want-item"
    result = runner.invoke(app, shlex.split(command_string))
    print(result.stdout.rstrip())
    assert result.exit_code == 0


@pytest.mark.component
def test_remote_peer_stats():
    """testing find_providers with native windows install"""
    command_string = "capture-remote-peer-stats"
    result = runner.invoke(app, shlex.split(command_string))
    print(result.stdout.rstrip())
    assert result.exit_code == 0


@pytest.mark.component
def test_want_list_swarm():
    """testing find_providers with native windows install"""
    command_string = "want-list-swarm"
    result = runner.invoke(app, shlex.split(command_string))
    print(result.stdout.rstrip())
    assert result.exit_code == 0
