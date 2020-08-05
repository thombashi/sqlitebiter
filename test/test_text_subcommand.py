"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from textwrap import dedent

from click.testing import CliRunner
from simplesqlite import SimpleSQLite

from sqlitebiter.__main__ import cmd
from sqlitebiter._const import ExitCode
from sqlitebiter.converter._base import SourceInfo

from .common import print_traceback
from .dataset import complex_json


class Test_stdin_subcommand:

    db_path = "test.sqlite"

    def test_normal_json(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(cmd, ["-o", self.db_path, "stdin", "json"], input=complex_json)
            print_traceback(result)
            assert result.exit_code == ExitCode.SUCCESS
            con = SimpleSQLite(self.db_path, "r")
            expected = {
                "ratings",
                "screenshots_4",
                "screenshots_3",
                "screenshots_5",
                "screenshots_1",
                "screenshots_2",
                "tags",
                "versions",
                "root",
                SourceInfo.get_table_name(),
            }
            assert set(con.fetch_table_names()) == expected

            result = runner.invoke(cmd, ["-o", self.db_path, "stdin", "csv"], input=complex_json)
            assert result.exit_code == ExitCode.FAILED_CONVERT

    def test_normal_type_hint_header(self):
        text = dedent(
            """\
            "a text","b integer","c real"
            1,"1","1.1"
            2,"2","1.2"
            3,"3","1.3"
            """
        )
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(
                cmd, ["--type-hint-header", "-o", self.db_path, "stdin", "csv"], input=text
            )
            print_traceback(result)
            assert result.exit_code == ExitCode.SUCCESS

            con = SimpleSQLite(self.db_path, "r")
            table_names = list(set(con.fetch_table_names()) - {SourceInfo.get_table_name()})

            # table name may change test execution order
            tbldata = con.select_as_tabledata(table_names[0])

            assert tbldata.headers == ["a text", "b integer", "c real"]
            assert tbldata.rows == [("1", 1, 1.1), ("2", 2, 1.2), ("3", 3, 1.3)]

    def test_smoke_max_workers(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(
                cmd, ["--max-workers", "4", "-o", self.db_path, "stdin", "json"], input=complex_json
            )

            assert result.exit_code == ExitCode.SUCCESS, file_path
