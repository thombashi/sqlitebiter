# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import print_function

import responses
import simplesqlite
from click.testing import CliRunner
from sqlitebiter._enum import ExitCode
from sqlitebiter.sqlitebiter import cmd

from .common import print_traceback
from .dataset import complex_json


class Test_TableUrlLoader(object):

    @responses.activate
    def test_normal(self):
        url = "https://example.com/complex_jeson.json"
        responses.add(
            responses.GET,
            url,
            body=complex_json,
            content_type='text/plain; charset=utf-8',
            status=200)
        runner = CliRunner()
        db_path = "test_complex_json.sqlite"

        with runner.isolated_filesystem():
            result = runner.invoke(cmd, ["url", url, "-o", db_path])
            print_traceback(result)

            assert result.exit_code == ExitCode.SUCCESS

            con = simplesqlite.SimpleSQLite(db_path, "r")
            expected = set([
                'ratings', 'screenshots_4', 'screenshots_3', 'screenshots_5', 'screenshots_1',
                'screenshots_2', 'tags', 'versions', 'root'])

            assert set(con.get_table_name_list()) == expected
