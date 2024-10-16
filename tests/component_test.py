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
    command_string = "capture-want-lists"
    result = runner.invoke(app, shlex.split(command_string))
    print(result.stdout.rstrip())
    assert result.exit_code == 0
