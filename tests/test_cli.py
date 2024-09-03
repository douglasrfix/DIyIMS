# from sys import stderr
from typer.testing import CliRunner

from diyims.diyims import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["test-app"])
    assert result.exit_code == 0
