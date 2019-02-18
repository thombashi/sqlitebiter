# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import print_function

import pytest
import responses
from click.testing import CliRunner
from simplesqlite import SimpleSQLite
from sqlitebiter._enum import ExitCode
from sqlitebiter.sqlitebiter import cmd
from sqlitebiter.subcommand._base import SourceInfo

from .common import print_traceback
from .dataset import complex_json


class Test_url_subcommand(object):

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
            expected = set(
                [
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
                ]
            )

            assert set(con.fetch_table_names()) == expected

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
