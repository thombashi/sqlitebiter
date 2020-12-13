from click.testing import CliRunner

from sqlitebiter.__main__ import cmd
from sqlitebiter._const import ExitCode

from .common import print_traceback


class Test_version_subcommand:
    def test_smoke(self):
        runner = CliRunner()
        result = runner.invoke(cmd, ["version"])
        print_traceback(result)

        assert result.exit_code == ExitCode.SUCCESS
