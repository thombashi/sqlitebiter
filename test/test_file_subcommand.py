# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import print_function

import os
from textwrap import dedent

import path
import pytest
import simplesqlite
from click.testing import CliRunner
from pytablereader.interface import TableLoader
from sqlitebiter._enum import ExitCode
from sqlitebiter.sqlitebiter import cmd
from sqliteschema import SqliteSchemaExtractor

from .common import print_test_result, print_traceback
from .dataset import *


class Test_sqlitebiter_file(object):

    def setup_method(self, method):
        TableLoader.clear_table_count()

    @pytest.mark.parametrize(["option_list", "expected"], [
        [["-h"], ExitCode.SUCCESS],
        [["file", "-h"], ExitCode.SUCCESS],
        [["gs", "-h"], ExitCode.SUCCESS],
    ])
    def test_help(self, option_list, expected):
        runner = CliRunner()
        result = runner.invoke(cmd, option_list)
        assert result.exit_code == expected

    @pytest.mark.parametrize(["file_creator", "expected"], [
        [valid_json_single_file, ExitCode.SUCCESS],
        [valid_json_multi_file_1, ExitCode.SUCCESS],
        [valid_json_kv_file, ExitCode.SUCCESS],
        [valid_csv_file_1_1, ExitCode.SUCCESS],
        [valid_csv_file_2_1, ExitCode.SUCCESS],
        [valid_tsv_file, ExitCode.SUCCESS],
        [valid_excel_file, ExitCode.SUCCESS],
        [valid_html_file, ExitCode.SUCCESS],
        [valid_ltsv_file, ExitCode.SUCCESS],
        [valid_markdown_file, ExitCode.SUCCESS],
        [valid_utf8_csv_file, ExitCode.SUCCESS],

        [invalid_csv_file, ExitCode.FAILED_CONVERT],
        [invalid_json_single_file, ExitCode.FAILED_CONVERT],
        [invalid_excel_file_1, ExitCode.NO_INPUT],
        [invalid_excel_file_2, ExitCode.FAILED_CONVERT],
        [invalid_html_file, ExitCode.NO_INPUT],
        [invalid_ltsv_file, ExitCode.FAILED_CONVERT],
        [invalid_tsv_file, ExitCode.FAILED_CONVERT],
        [not_supported_format_file, ExitCode.FAILED_CONVERT],
    ])
    def test_smoke_one_file(self, file_creator, expected):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_path = file_creator()
            result = runner.invoke(cmd, ["file", file_path, "-o", db_path])

            assert result.exit_code == expected, file_path

    @pytest.mark.parametrize(["file_creator", "test_path", "file_format", "expected"], [
        [valid_csv_file_1_1, "without_ext", "csv", ExitCode.SUCCESS],
        [valid_csv_file_1_1, "without_ext", "excel", ExitCode.FAILED_CONVERT],
        [valid_csv_file_1_1, "unmatch_ext.json", "csv", ExitCode.SUCCESS],
    ])
    def test_smoke_format(self, test_path, file_creator, file_format, expected):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_path = file_creator()
            os.rename(file_path, test_path)
            result = runner.invoke(
                cmd, ["file", test_path, "--format", file_format, "-o", db_path])

            assert result.exit_code == expected, file_path

    def test_smoke_multi_file(self):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_list = [
                valid_json_single_file(),
                valid_json_multi_file_1(),
                valid_csv_file_1_1(),
                valid_csv_file_2_1(),
                valid_tsv_file(),
                valid_excel_file(),
                valid_html_file(),
                valid_ltsv_file(),
                valid_markdown_file(),
                valid_utf8_csv_file(),
                valid_utf16_csv_file(),
            ]

            result = runner.invoke(cmd, ["file"] + file_list + ["-o", db_path])

            assert result.exit_code == ExitCode.SUCCESS

    @pytest.mark.parametrize(
        ["file_creator", "verbosity_option", "expected"],
        [
            [valid_csv_file_1_1, "-v", ExitCode.SUCCESS],
            [valid_csv_file_1_1, "-vv", ExitCode.SUCCESS],
            [valid_csv_file_1_1, "-vvv", ExitCode.SUCCESS],
        ])
    def test_smoke_verbose(self, file_creator, verbosity_option, expected):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_path = file_creator()
            result = runner.invoke(cmd, [verbosity_option, "file", file_path, "-o", db_path])

            assert result.exit_code == expected, file_path

    def test_abnormal_empty(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(cmd, ["file"])

            assert result.exit_code == ExitCode.NO_INPUT
            assert not path.Path("out.sqlite").exists(), "output file must not exist"

    def test_abnormal_smoke(self):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_list = [
                invalid_csv_file(),
                invalid_json_single_file(),
                invalid_excel_file_1(),
                invalid_excel_file_2(),
                invalid_html_file(),
                invalid_ltsv_file(),
                invalid_tsv_file(),
                not_supported_format_file(),
            ]

            for file_path in file_list:
                result = runner.invoke(cmd, ["file", file_path, "-o", db_path])

                assert result.exit_code in (ExitCode.FAILED_CONVERT, ExitCode.NO_INPUT), file_path

    @pytest.mark.parametrize(["file_creator", "expected"], [
        [valid_excel_file_1, ExitCode.SUCCESS],
    ])
    def test_normal_one_file(self, file_creator, expected):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_path = file_creator()
            result = runner.invoke(cmd, ["file", file_path, "-o", db_path])

            assert result.exit_code == expected, file_path

    def test_normal_multi_file_different_table(self):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_list = [
                valid_json_single_file(),
                invalid_json_single_file(),

                valid_json_multi_file_1(),
                valid_json_kv_file(),

                valid_csv_file_1_1(),
                valid_csv_file_2_1(),
                invalid_csv_file(),

                valid_tsv_file(),
                invalid_tsv_file(),

                valid_excel_file(),
                invalid_excel_file_1(),
                invalid_excel_file_2(),

                valid_html_file(),
                invalid_html_file(),

                valid_ltsv_file(),
                invalid_ltsv_file(),

                valid_markdown_file(),

                not_supported_format_file(),
            ]

            result = runner.invoke(cmd, ["file"] + file_list + ["-o", db_path])
            assert result.exit_code == ExitCode.SUCCESS

            con = simplesqlite.SimpleSQLite(db_path, "r")
            expected_table_list = [
                'singlejson', 'multij1', 'multij2', "valid_kv",
                'csv_a', "rename_insert",
                'excel_sheet_a', 'excel_sheet_c', 'excel_sheet_d',
                "valid_ltsv_a",
                'testtitle_tablename', 'testtitle_html2',
                'tsv_a',
                'valid_mdtable_markdown1',
            ]
            actual_table_list = con.get_table_name_list()

            print_test_result(expected=expected_table_list, actual=actual_table_list)

            assert set(actual_table_list) == set(expected_table_list)

            expected_data_table = {
                "singlejson": [(1, 4.0, 'a'), (2, 2.1, 'bb'), (3, 120.9, 'ccc')],
                "multij1": [(1, 4.0, 'a'), (2, 2.1, 'bb'), (3, 120.9, 'ccc')],
                "multij2": [(1, 4.0), (2, None), (3, 120.9)],
                "valid_kv": [('json_b', 'hoge'), ('json_c', 'bar')],
                "csv_a": [(1, 4.0, 'a'), (2, 2.1, 'bb'), (3, 120.9, 'ccc')],
                "rename_insert": [
                    (1, 55, 'D Sam', 31, 'Raven'),
                    (2, 36, 'J Ifdgg', 30, 'Raven'),
                    (3, 91, 'K Wedfb', 28, 'Raven'),
                ],
                "excel_sheet_a": [(1.0, 1.1, 'a'), (2.0, 2.2, 'bb'), (3.0, 3.3, 'cc')],
                "excel_sheet_c": [(1, 1.1, 'a'), (2, '', 'bb'), (3, 3.3, '')],
                "excel_sheet_d": [(1, 1.1, 'a'), (2, '', 'bb'), (3, 3.3, '')],
                "testtitle_tablename": [(1, 123.1, 'a'), (2, 2.2, 'bb'), (3, 3.3, 'ccc')],

                "valid_ltsv_a": [
                    (1, 123.1, u'"ltsv0"', 1.0, u'"1"'),
                    (2, 2.2, u'"ltsv1"', 2.2, u'"2.2"'),
                    (3, 3.3, u'"ltsv2"', 3.0, u'"cccc"'),
                ],
                "testtitle_html2": [(1, 123.1), (2, 2.2), (3, 3.3)],
                "tsv_a": [(1, 4.0, 'tsv0'), (2, 2.1, 'tsv1'), (3, 120.9, 'tsv2')],
                "valid_mdtable_markdown1": [(1, 123.1, 'a'), (2, 2.2, 'bb'), (3, 3.3, 'ccc')],
            }
            for table in con.get_table_name_list():
                result = con.select("*", table_name=table)
                expected_data = expected_data_table.get(table)
                actual_data = result.fetchall()

                message = "table={}, expected={}, actual={}".format(
                    table, expected_data, actual_data)

                print("--- table: {} ---".format(table))
                print_test_result(expected=expected_data, actual=actual_data)

                assert expected_data == actual_data, message

    def test_normal_format_ssv(self):
        db_path = "test_ssv.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_path = valid_ssv_file()
            result = runner.invoke(cmd, ["file", file_path, "-o", db_path, "--format", "ssv"])
            print_traceback(result)

            assert result.exit_code == ExitCode.SUCCESS

            con = simplesqlite.SimpleSQLite(db_path, "r")
            data = con.select_as_tabledata(table_name="ssv")
            expected = (
                "table_name=ssv, "
                "header_list=[USER, PID, CPU, MEM, VSZ, RSS, TTY, STAT, START, TIME, COMMAND], "
                "rows=5")

            assert str(data) == expected

    @pytest.mark.parametrize(["file_creator", "index_list", "expected"], [
        [
            valid_csv_file_3_1, "aa,ac",
            dedent("""\
                .. table:: valid_csv_3_1 (3 records)

                    +--------------+---------+-----------+--------+------+-----+
                    |Attribute name|Data type|Primary key|Not NULL|Unique|Index|
                    +==============+=========+===========+========+======+=====+
                    |aa            |REAL     |           |        |      |X    |
                    +--------------+---------+-----------+--------+------+-----+
                    |ab            |INTEGER  |           |        |      |     |
                    +--------------+---------+-----------+--------+------+-----+
                    |ac            |TEXT     |           |        |      |X    |
                    +--------------+---------+-----------+--------+------+-----+

                """)
        ],
    ])
    def test_normal_index(self, file_creator, index_list, expected):
        db_path = "test_index.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_path = file_creator()
            result = runner.invoke(cmd, ["--index", index_list, "file", file_path, "-o", db_path])
            print_traceback(result)

            assert result.exit_code == ExitCode.SUCCESS

            extractor = SqliteSchemaExtractor(db_path)

            print_test_result(expected=expected, actual=extractor.dumps())

            assert extractor.dumps() == expected

    def test_normal_append(self):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_list = [
                valid_json_multi_file_2_1(),
            ]
            table_name = "multij2"
            expected_table_list = [table_name]

            # first execution without --append option (new) ---
            result = runner.invoke(cmd, ["file"] + file_list + ["-o", db_path])
            print_traceback(result)
            assert result.exit_code == ExitCode.SUCCESS

            con = simplesqlite.SimpleSQLite(db_path, "r")

            actual_table_list = con.get_table_name_list()

            print_test_result(expected=expected_table_list, actual=actual_table_list)

            assert set(actual_table_list) == set(expected_table_list)

            actual_data = con.select("*", table_name=table_name).fetchall()
            expected_data = [
                (1, 4.0, 'a'),
                (2, 2.1, 'bb'),
                (3, 120.9, 'ccc'),
            ]

            print_test_result(expected=expected_data, actual=actual_data)

            assert expected_data == actual_data

            # second execution with --append option ---
            result = runner.invoke(
                cmd, ["--append", "file"] + file_list + ["-o", db_path])
            print_traceback(result)
            assert result.exit_code == ExitCode.SUCCESS

            con = simplesqlite.SimpleSQLite(db_path, "r")

            actual_table_list = con.get_table_name_list()

            print_test_result(expected=expected_table_list, actual=actual_table_list)

            assert set(actual_table_list) == set(expected_table_list)

            actual_data = con.select("*", table_name=table_name).fetchall()
            expected_data = [
                (1, 4.0, 'a'),
                (2, 2.1, 'bb'),
                (3, 120.9, 'ccc'),
                (1, 4.0, 'a'),
                (2, 2.1, 'bb'),
                (3, 120.9, 'ccc'),
            ]

            print_test_result(expected=expected_data, actual=actual_data)

            assert expected_data == actual_data

            # third execution without --append option (overwrite) ---
            result = runner.invoke(cmd, ["file"] + file_list + ["-o", db_path])
            print_traceback(result)
            assert result.exit_code == ExitCode.SUCCESS

            con = simplesqlite.SimpleSQLite(db_path, "r")

            actual_table_list = con.get_table_name_list()

            print_test_result(expected=expected_table_list, actual=actual_table_list)

            assert set(actual_table_list) == set(expected_table_list)

            actual_data = con.select("*", table_name=table_name).fetchall()
            expected_data = [
                (1, 4.0, 'a'),
                (2, 2.1, 'bb'),
                (3, 120.9, 'ccc'),
            ]

            print_test_result(expected=expected_data, actual=actual_data)

            assert expected_data == actual_data

    def test_normal_multi_file_same_table_same_structure(self):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_list = [
                valid_json_multi_file_2_1(),
                valid_json_multi_file_2_2(),
            ]

            result = runner.invoke(cmd, ["file"] + file_list + ["-o", db_path])
            print_traceback(result)
            assert result.exit_code == ExitCode.SUCCESS

            con = simplesqlite.SimpleSQLite(db_path, "r")
            expected_table_list = ['multij2']
            actual_table_list = con.get_table_name_list()

            print_test_result(expected=expected_table_list, actual=actual_table_list)

            assert set(actual_table_list) == set(expected_table_list)

            expected_data_table = {
                "multij2": [
                    (1, 4.0, 'a'),
                    (2, 2.1, 'bb'),
                    (3, 120.9, 'ccc'),
                    (1, 4.0, 'a'),
                    (2, 2.1, 'bb'),
                    (3, 120.9, 'ccc'),
                ],
            }

            for table in con.get_table_name_list():
                expected_data = expected_data_table.get(table)
                actual_data = con.select("*", table_name=table).fetchall()

                message = "table={}, expected={}, actual={}".format(
                    table, expected_data, actual_data)

                print("--- table: {} ---".format(table))
                print_test_result(expected=expected_data, actual=actual_data)

                assert expected_data == actual_data, message

    def test_normal_multi_file_same_table_different_structure(self):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_list = [
                valid_json_multi_file_2_2(),
                valid_json_multi_file_2_3(),
            ]

            result = runner.invoke(cmd, ["file"] + file_list + ["-o", db_path])
            print_traceback(result)
            assert result.exit_code == ExitCode.SUCCESS

            con = simplesqlite.SimpleSQLite(db_path, "r")
            expected_table_list = ['multij2', 'multij2_1']
            actual_table_list = con.get_table_name_list()

            print_test_result(expected=expected_table_list, actual=actual_table_list)

            assert set(actual_table_list) == set(expected_table_list)

            expected_data_table = {
                "multij2": [
                    (1, 4.0, 'a'),
                    (2, 2.1, 'bb'),
                    (3, 120.9, 'ccc'),
                ],
                "multij2_1": [
                    (u'abc', u'a', 4.0),
                    (u'abc', u'bb', 2.1),
                    (u'abc', u'ccc', 120.9),
                ],
            }

            for table in con.get_table_name_list():
                expected_data = expected_data_table.get(table)
                actual_data = con.select("*", table_name=table).fetchall()

                message = "table={}, expected={}, actual={}".format(
                    table, expected_data, actual_data)

                print("--- table: {} ---".format(table))
                print_test_result(expected=expected_data, actual=actual_data)

                assert expected_data == actual_data, message

    def test_normal_complex_json(self):
        db_path = "test_complex_json.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_path = valid_complex_json_file()
            result = runner.invoke(cmd, ["file", file_path, "-o", db_path])
            print_traceback(result)

            assert result.exit_code == ExitCode.SUCCESS

            con = simplesqlite.SimpleSQLite(db_path, "r")
            expected = set([
                'ratings', 'screenshots_4', 'screenshots_3', 'screenshots_5', 'screenshots_1',
                'screenshots_2', 'tags', 'versions', 'root'])

            assert set(con.get_table_name_list()) == expected
