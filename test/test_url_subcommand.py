# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import print_function

import pytest
import responses
import simplesqlite
from click.testing import CliRunner
from sqlitebiter._enum import ExitCode
from sqlitebiter.sqlitebiter import cmd

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
            content_type='text/plain; charset=utf-8',
            status=200)
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(cmd, ["url", url, "-o", self.db_path])
            print_traceback(result)

            assert result.exit_code == ExitCode.SUCCESS

            con = simplesqlite.SimpleSQLite(self.db_path, "r")
            expected = set([
                'ratings', 'screenshots_4', 'screenshots_3', 'screenshots_5', 'screenshots_1',
                'screenshots_2', 'tags', 'versions', 'root'])

            assert set(con.get_table_name_list()) == expected

    @pytest.mark.parametrize(["url", "expected"], [
        [
            "https://en.wikipedia.org/wiki/Comparison_of_firewalls",
            ExitCode.SUCCESS,
        ], [
            "https://en.wikipedia.org/wiki/Comparison_of_firewalls#Firewall_software",
            ExitCode.SUCCESS,
        ],
    ])
    def test_normal_html(self, url, expected):
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(cmd, ["url", url, "-o", self.db_path])
            print_traceback(result)

            assert result.exit_code == expected
