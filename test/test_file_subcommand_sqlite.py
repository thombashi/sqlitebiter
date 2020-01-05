# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import print_function

import pytest
from click.testing import CliRunner
from pytablereader import SqliteFileLoader
from simplesqlite import SimpleSQLite
from tabledata import TableData

from sqlitebiter._const import ExitCode
from sqlitebiter.sqlitebiter import cmd
from sqlitebiter.subcommand._base import SourceInfo

from .common import print_traceback


TEST_TABLE_NAME_A = "test_table_a"
TEST_TABLE_NAME_B = "test_table_b"


@pytest.fixture
def con_a0():
    con = SimpleSQLite("tmp_a0.sqlite", "w")
    con.create_table_from_data_matrix(TEST_TABLE_NAME_A, ["attr_a", "attr_b"], [[1, 2], [3, 4]])

    return con


@pytest.fixture
def con_a1():
    con = SimpleSQLite("tmp_a1.sqlite", "w")
    con.create_table_from_data_matrix(TEST_TABLE_NAME_A, ["attr_a", "attr_b"], [[11, 12], [13, 14]])

    return con


@pytest.fixture
def con_b0():
    con = SimpleSQLite("tmp_b0.sqlite", "w")
    con.create_table_from_data_matrix(TEST_TABLE_NAME_B, ["ba", "bb"], [[101, 102], [103, 104]])

    return con


class Test_sqlitebiter_file_sqlite_merge(object):
    def test_normal_same_table(self, con_a0, con_a1):
        out_db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(
                cmd, ["-o", out_db_path, "file", con_a0.database_path, con_a1.database_path]
            )
            print_traceback(result)
            assert result.exit_code == ExitCode.SUCCESS

            expected = TableData(
                TEST_TABLE_NAME_A, ["attr_a", "attr_b"], [[1, 2], [3, 4], [11, 12], [13, 14]]
            )
            for tabledata in SqliteFileLoader(out_db_path).load():
                if tabledata.table_name == SourceInfo.get_table_name():
                    continue

                assert tabledata == expected

    def test_normal_multi_table(self, con_a0, con_b0):
        out_db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(
                cmd, ["-o", out_db_path, "file", con_a0.database_path, con_b0.database_path]
            )
            print_traceback(result)
            assert result.exit_code == ExitCode.SUCCESS

            expected_list = [
                TableData(TEST_TABLE_NAME_A, ["attr_a", "attr_b"], [[1, 2], [3, 4]]),
                TableData(TEST_TABLE_NAME_B, ["ba", "bb"], [[101, 102], [103, 104]]),
            ]
            for tabledata in SqliteFileLoader(out_db_path).load():
                if tabledata.table_name == SourceInfo.get_table_name():
                    continue

                print("[actual]\n{}".format(tabledata))
                for record in tabledata.value_matrix:
                    print("  {}".format(record))

                assert tabledata in expected_list
