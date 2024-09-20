import os
import shlex

import pytest
from typer.testing import CliRunner

from diyims.diyims import app

runner = CliRunner()


@pytest.fixture(scope="function")
def environ_h(tmp_path):
    p = str(tmp_path)
    os.environ["OVERRIDE_HOME"] = p


@pytest.fixture(scope="function")
def environ_p(monkeypatch):
    monkeypatch.setenv("OVERRIDE_PLATFORM", "unknown")


# @pytest.mark.skip(reason="menus")
def test_cli_l1_c0():
    """runner can't test the l1 command with noargs =true"""
    command_string = "diyims"
    result = runner.invoke(app, shlex.split(command_string))
    print(result.stdout.rstrip())
    assert result.exit_code == 2


# @pytest.mark.skip(reason="menus")


def test_cli_l1_c1():
    """runner can't test the l1 commands with the
    diyims command the you would form the command line"""
    command_string = "diyims install-utils"
    result = runner.invoke(app, shlex.split(command_string))
    print(result.stdout.rstrip())
    assert result.exit_code == 2


# @pytest.mark.skip(reason="menus")
def test_cli_l2_c0():
    command_string = "install-utils"
    result = runner.invoke(app, shlex.split(command_string))
    print(result.stdout.rstrip())
    assert result.exit_code == 0


# @pytest.mark.skip(reason="menus")


def test_cli_l2_c1_a():
    """testing  install with no option windows 11
    this should also be okay for windows 10
    will also test envrion not exist"""
    command_string = "install-utils install"
    result = runner.invoke(app, shlex.split(command_string))
    print(result.stdout.rstrip())
    assert result.exit_code == 1


# @pytest.mark.skip(reason="menus")


def test_cli_l2_c1_ab(environ_p):
    """testing  install with no option windows 11
    this should also be okay for windows 10
    will test unsupported platform"""
    command_string = "install-utils install"
    result = runner.invoke(app, shlex.split(command_string))
    print(result.stdout.rstrip())
    assert result.exit_code == 2


# @pytest.mark.skip(reason="menus")
def test_cli_l2_c1_b(environ_h):
    """testing  install with --force option windows 11
    this should also be okay for windows 10  also test default drive letter"""
    command_string = "install-utils install --force-python"
    result = runner.invoke(app, shlex.split(command_string))
    print(result.stdout.rstrip())
    assert result.exit_code == 0


# @pytest.mark.skip(reason="menus")


def test_cli_l2_c1_n(environ_h):
    """testing  install with --force option windows 11
    this should also be okay for windows 10  also test default drive letter"""
    command_string = "install-utils install --force-python"
    result = runner.invoke(app, shlex.split(command_string))
    print(result.stdout.rstrip())
    assert result.exit_code == 0


# @pytest.mark.skip(reason="menus")
def test_cli_l2_c1_c(environ_h):
    """testing  install with --force option windows 11
    this should also be okay for windows 10"""
    command_string = "install-utils install --force-python --drive-letter 'D'"
    result = runner.invoke(app, shlex.split(command_string))
    print(result.stdout.rstrip())
    assert result.exit_code == 2


# @pytest.mark.skip(reason="menus")
def test_cli_l2_c1_d(environ_h):
    """testing  install with --force option windows 11
    this should also be okay for windows 10"""
    command_string = "install-utils install --force-python --drive-letter 'C'"
    result = runner.invoke(app, shlex.split(command_string))
    print(result.stdout.rstrip())
    assert result.exit_code == 0
