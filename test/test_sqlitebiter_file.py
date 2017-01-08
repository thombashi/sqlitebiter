# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import unicode_literals
from __future__ import print_function

from click.testing import CliRunner
import path
import pytest
import simplesqlite

from sqlitebiter._enum import ExitCode
from sqlitebiter.sqlitebiter import cmd
from pytablereader.interface import TableLoader

from .dataset import (
    valid_json_single_file,
    invalid_json_single_file,
    valid_json_multi_file,
    invalid_json_multi_file,
    valid_csv_file_1,
    valid_csv_file_2,
    invalid_csv_file,
    valid_tsv_file,
    invalid_tsv_file,
    valid_excel_file,
    invalid_excel_file_1,
    invalid_excel_file_2,
    valid_html_file,
    invalid_html_file,
    valid_ltsv_file,
    invalid_ltsv_file,
    valid_markdown_file,
    valid_multibyte_char_file,
    not_supported_format_file,
)


class Test_sqlitebiter_file:

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
        [valid_json_multi_file, ExitCode.SUCCESS],
        [valid_csv_file_1, ExitCode.SUCCESS],
        [valid_csv_file_2, ExitCode.SUCCESS],
        [valid_tsv_file, ExitCode.SUCCESS],
        [valid_excel_file, ExitCode.SUCCESS],
        [valid_html_file, ExitCode.SUCCESS],
        [valid_ltsv_file, ExitCode.SUCCESS],
        [valid_markdown_file, ExitCode.SUCCESS],
        [valid_multibyte_char_file, ExitCode.SUCCESS],

        [invalid_csv_file, ExitCode.FAILED_CONVERT],
        [invalid_json_single_file, ExitCode.FAILED_CONVERT],
        [invalid_json_multi_file, ExitCode.FAILED_CONVERT],
        [invalid_excel_file_1, ExitCode.NO_INPUT],
        [invalid_excel_file_2, ExitCode.FAILED_CONVERT],
        [invalid_html_file, ExitCode.NO_INPUT],
        [invalid_ltsv_file, ExitCode.FAILED_CONVERT],
        [invalid_tsv_file, ExitCode.FAILED_CONVERT],
        [not_supported_format_file, ExitCode.FAILED_CONVERT],
    ])
    def test_normal_one_file(self, file_creator, expected):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_path = file_creator()
            result = runner.invoke(
                cmd, ["file", file_path, "-o", db_path])
            assert result.exit_code == expected, file_path

    def test_normal_multi_file(self):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_list = [
                valid_json_single_file(),
                valid_json_multi_file(),
                valid_csv_file_1(),
                valid_csv_file_2(),
                valid_tsv_file(),
                valid_excel_file(),
                valid_html_file(),
                valid_ltsv_file(),
                valid_markdown_file(),
                valid_multibyte_char_file(),
            ]

            result = runner.invoke(cmd, ["file"] + file_list + ["-o", db_path])

            assert result.exit_code == ExitCode.SUCCESS

    @pytest.mark.parametrize(
        ["file_creator", "verbosity_option", "expected"],
        [
            [valid_csv_file_1, "-v", ExitCode.SUCCESS],
            [valid_csv_file_1, "-vv", ExitCode.SUCCESS],
            [valid_csv_file_1, "-vvv", ExitCode.SUCCESS],
        ]
    )
    def test_smoke_verbose(self, file_creator, verbosity_option, expected):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_path = file_creator()
            result = runner.invoke(
                cmd, [verbosity_option, "file", file_path, "-o", db_path])
            assert result.exit_code == expected, file_path

    @pytest.mark.parametrize(
        ["file_creator", "verbosity_option", "expected"],
        [
            [valid_csv_file_1, "--quiet", ExitCode.SUCCESS],
        ]
    )
    def test_smoke_quiet(
            self, capsys, file_creator, verbosity_option, expected):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_path = file_creator()
            result = runner.invoke(
                cmd, [verbosity_option, "file", file_path, "-o", db_path])

            assert result.exit_code == expected, file_path

            out, _err = capsys.readouterr()

            assert out.strip() == ""

    def test_abnormal_empty(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(
                cmd, ["file"])

            assert result.exit_code == ExitCode.NO_INPUT
            assert not path.Path(
                "out.sqlite").exists(), "output file must not exist"

    def test_abnormal_smoke(self):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_list = [
                invalid_csv_file(),
                invalid_json_single_file(),
                invalid_json_multi_file(),
                invalid_excel_file_1(),
                invalid_excel_file_2(),
                invalid_html_file(),
                invalid_ltsv_file(),
                invalid_tsv_file(),
                not_supported_format_file(),
            ]

            for file_path in file_list:
                result = runner.invoke(
                    cmd, ["file", file_path, "-o", db_path])

                assert result.exit_code in (
                    ExitCode.FAILED_CONVERT, ExitCode.NO_INPUT), file_path

    def test_normal_multi(self):
        db_path = "test.sqlite"
        runner = CliRunner()
        with runner.isolated_filesystem():
            file_list = [
                valid_json_single_file(),
                invalid_json_single_file(),

                valid_json_multi_file(),
                invalid_json_multi_file(),

                valid_csv_file_1(),
                valid_csv_file_2(),
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
            expected_tables = [
                'singlejson_json1', 'multijson_table1', 'multijson_table2',
                'csv_a', "rename_insert",
                'excel_sheet_a', 'excel_sheet_c', 'excel_sheet_d',
                "valid_ltsv_a",
                'testtitle_tablename', 'testtitle_html2',
                'tsv_a',
                'valid_mdtable_markdown1',
            ]

            message = "expected-tables={}, actual-tables={}".format(
                expected_tables, con.get_table_name_list())
            assert set(con.get_table_name_list()) == set(
                expected_tables), message

            expected_data_table = {
                "singlejson_json1":
                    [(1, 4.0, 'a'), (2, 2.1, 'bb'), (3, 120.9, 'ccc')],
                "multijson_table1":
                    [(1, 4.0, 'a'), (2, 2.1, 'bb'), (3, 120.9, 'ccc')],
                "multijson_table2":
                    [(1, 4.0), (2, None), (3, 120.9)],
                "csv_a": [(1, 4.0, 'a'), (2, 2.1, 'bb'), (3, 120.9, 'ccc')],
                "rename_insert": [
                    (1, 55, 'D Sam', 31, 'Raven'),
                    (2, 36, 'J Ifdgg', 30, 'Raven'),
                    (3, 91, 'K Wedfb', 28, 'Raven'),
                ],
                "excel_sheet_a":
                    [(1.0, 1.1, 'a'), (2.0, 2.2, 'bb'), (3.0, 3.3, 'cc')],
                "excel_sheet_c":
                    [(1, 1.1, 'a'), (2, '', 'bb'), (3, 3.3, '')],
                "excel_sheet_d":
                    [(1, 1.1, 'a'), (2, '', 'bb'), (3, 3.3, '')],
                "testtitle_tablename":
                    [(1, 123.1, 'a'), (2, 2.2, 'bb'), (3, 3.3, 'ccc')],

                "valid_ltsv_a": [
                    (1, 123.1, u'ltsv0', 1.0, u'1'),
                    (2, 2.2, u'ltsv1', 2.2, u'2.2'),
                    (3, 3.3, u'ltsv2', 3.0, u'cccc'),
                ],
                "testtitle_html2":
                    [(1, 123.1), (2, 2.2), (3, 3.3)],
                "tsv_a":
                    [(1, 4.0, 'tsv0'), (2, 2.1, 'tsv1'), (3, 120.9, 'tsv2')],
                "valid_mdtable_markdown1":
                    [(1, 123.1, 'a'), (2, 2.2, 'bb'), (3, 3.3, 'ccc')],
            }
            for table in con.get_table_name_list():
                result = con.select("*", table_name=table)
                expected_data = expected_data_table.get(table)
                actual_data = result.fetchall()

                message = "table={}, expected={}, actual={}".format(
                    table, expected_data, actual_data)

                print("--- table: {} ---".format(table))
                print("[expected]\n{}\n".format(expected_data))
                print("[actual]\n{}\n".format(actual_data))

                assert expected_data == actual_data, message
