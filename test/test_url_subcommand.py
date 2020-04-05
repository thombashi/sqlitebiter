"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from textwrap import dedent

import pytest
import responses
from click.testing import CliRunner
from simplesqlite import SimpleSQLite

from sqlitebiter.__main__ import cmd
from sqlitebiter._const import ExitCode
from sqlitebiter.converter._base import SourceInfo

from .common import print_traceback
from .dataset import complex_json


class Test_url_subcommand:

    db_path = "test.sqlite"

    @responses.activate
    def test_normal_json(self):
        url = "https://example.com/complex_json.json"
        responses.add(
            responses.GET,
            url,
            body=complex_json,
            content_type="text/plain; charset=utf-8",
            status=200,
        )
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(cmd, ["-o", self.db_path, "url", url])
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

    @responses.activate
    def test_normal_type_hint_header(self):
        url = "https://example.com/type_hint_header.csv"
        responses.add(
            responses.GET,
            url,
            body=dedent(
                """\
                "a text","b integer","c real"
                1,"1","1.1"
                2,"2","1.2"
                3,"3","1.3"
                """
            ),
            content_type="text/plain; charset=utf-8",
            status=200,
        )
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(cmd, ["--type-hint-header", "-o", self.db_path, "url", url])
            print_traceback(result)
            assert result.exit_code == ExitCode.SUCCESS

            con = SimpleSQLite(self.db_path, "r")
            table_names = list(set(con.fetch_table_names()) - {SourceInfo.get_table_name()})

            # table name may change test execution order
            tbldata = con.select_as_tabledata(table_names[0])

            assert tbldata.headers == ["a text", "b integer", "c real"]
            assert tbldata.rows == [("1", 1, 1.1), ("2", 2, 1.2), ("3", 3, 1.3)]

    @pytest.mark.xfail(run=False)
    @pytest.mark.parametrize(
        ["url", "expected"],
        [
            ["https://en.wikipedia.org/wiki/Comparison_of_firewalls", ExitCode.SUCCESS],
            [
                "https://en.wikipedia.org/wiki/Comparison_of_firewalls#Firewall_software",
                ExitCode.SUCCESS,
            ],
        ],
    )
    def test_normal_html(self, url, expected):
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(cmd, ["-o", self.db_path, "url", url])
            print_traceback(result)

            assert result.exit_code == expected

    @pytest.mark.xfail(run=False)
    @pytest.mark.parametrize(
        ["url", "expected"],
        [
            [
                "https://raw.githubusercontent.com/fastai/fastai/master/old/tutorials/meanshift.ipynb",
                ExitCode.SUCCESS,
            ],
            [
                "https://raw.githubusercontent.com/fastai/fastai/master/old/tutorials/linalg_pytorch.ipynb",
                ExitCode.SUCCESS,
            ],
            [
                "https://raw.githubusercontent.com/aymericdamien/TensorFlow-Examples/master/notebooks/1_Introduction/basic_eager_api.ipynb",
                ExitCode.SUCCESS,
            ],
            [
                "https://raw.githubusercontent.com/aymericdamien/TensorFlow-Examples/master/notebooks/3_NeuralNetworks/recurrent_network.ipynb",
                ExitCode.SUCCESS,
            ],
        ],
    )
    def test_smoke_url_ipynb(self, url, expected):
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(cmd, ["-o", self.db_path, "url", url])
            print_traceback(result)

            assert result.exit_code == expected
