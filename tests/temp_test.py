import shlex


from typer.testing import CliRunner

from diyims.diyims import app

runner = CliRunner()


def test_temp_test():
    """testing  general install 'real path'process for linux and unspecified drive letter"""
    command_string = "temp-test"
    result = runner.invoke(app, shlex.split(command_string))
    print(result.stdout.rstrip())
    assert result.exit_code == 0