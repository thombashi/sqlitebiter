"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""


import os
from textwrap import dedent

import path
import pytest
from click.testing import CliRunner
from pytablereader.interface import AbstractTableReader
from simplesqlite import SimpleSQLite
from sqliteschema import SQLiteSchemaExtractor

from sqlitebiter._const import ExitCode
from sqlitebiter.converter._base import SourceInfo
from sqlitebiter.sqlitebiter import cmd

from .common import print_test_result, print_traceback
from .dataset import *


class Test_sqlitebiter_file:
    def setup_method(self, method):
        AbstractTableReader.clear_table_count()

    @pytest.mark.parametrize(
        ["options", "expected"],
        [
            [["-h"], ExitCode.SUCCESS],
            [["file", "-h"], ExitCode.SUCCESS],
            [["gs", "-h"], ExitCode.SUCCESS],
        ],
    )
    def test_help(self, options, expected):
        runner = CliRunner()
        result = runner.invoke(cmd, options)
        assert result.exit_code == expected

    @pytest.mark.parametrize(
        ["file_creator", "expected"],
        [
            [valid_json_single_file, ExitCode.SUCCESS],
            [valid_json_multi_file_1, ExitCode.SUCCESS],
            [valid_json_kv_file, ExitCode.SUCCESS],
            [valid_jsonlines_file, ExitCode.SUCCESS],
            [valid_csv_file_1_1, ExitCode.SUCCESS],
            [valid_csv_file_2_1, ExitCode.SUCCESS],
            [valid_tsv_file, ExitCode.SUCCESS],
            [valid_excel_file, ExitCode.SUCCESS],
            [valid_html_file, ExitCode.SUCCESS],
            [valid_ltsv_file, ExitCode.SUCCESS],
            [valid_markdown_file, ExitCode.SUCCESS],
            [valid_utf8_csv_file, ExitCode.SUCCESS],
            [valid_json_symbols, ExitCode.SUCCESS],
            [invalid_csv_file, ExitCode.FAILED_CONVERT],
            [valid_json_single_b_file, ExitCode.SUCCESS],
            [invalid_excel_file_1, ExitCode.NO_INPUT],
            [invalid_excel_file_2, ExitCode.FAILED_CONVERT],
            [invalid_html_file, ExitCode.NO_INPUT],
            [invalid_ltsv_file, ExitCode.FAILED_CONVERT],
            [invalid_tsv_file, ExitCode.FAILED_CONVERT],
            [not_supported_format_file, ExitCode.FAILED_CONVERT],
        ],
    )
    def test_smoke_one_file(self, file_creator, expected):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_path = file_creator()
            result = runner.invoke(cmd, ["-o", db_path, "file", file_path])
            print_traceback(result)

            assert result.exit_code == expected, file_path

    @pytest.mark.parametrize(
        ["file_creator", "test_path", "file_format", "expected"],
        [
            [valid_csv_file_1_1, "without_ext", "csv", ExitCode.SUCCESS],
            [valid_csv_file_1_1, "without_ext", "excel", ExitCode.FAILED_CONVERT],
            [valid_csv_file_1_1, "unmatch_ext.json", "csv", ExitCode.SUCCESS],
        ],
    )
    def test_smoke_format(self, test_path, file_creator, file_format, expected):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_path = file_creator()
            os.rename(file_path, test_path)
            result = runner.invoke(cmd, ["-o", db_path, "file", test_path, "--format", file_format])

            assert result.exit_code == expected, file_path

    def test_smoke_multi_file(self):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            files = [
                valid_json_single_file(),
                valid_json_single_b_file(),
                valid_json_multi_file_1(),
                valid_jsonlines_file(),
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

            result = runner.invoke(cmd, ["-o", db_path, "file"] + files)

            assert result.exit_code == ExitCode.SUCCESS

    @pytest.mark.parametrize(
        ["file_creator", "verbosity_option", "expected"],
        [
            [valid_csv_file_1_1, "-v", ExitCode.SUCCESS],
            [valid_csv_file_1_1, "-vv", ExitCode.SUCCESS],
            [valid_csv_file_1_1, "-vvv", ExitCode.SUCCESS],
            [valid_csv_file_1_1, "--quiet", ExitCode.SUCCESS],
        ],
    )
    def test_smoke_verbose(self, file_creator, verbosity_option, expected):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_path = file_creator()
            result = runner.invoke(cmd, [verbosity_option, "-o", db_path, "file", file_path])

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
            files = [
                invalid_csv_file(),
                invalid_excel_file_1(),
                invalid_excel_file_2(),
                invalid_html_file(),
                invalid_ltsv_file(),
                invalid_tsv_file(),
                not_supported_format_file(),
            ]

            for file_path in files:
                result = runner.invoke(cmd, ["-o", db_path, "file", file_path])

                assert result.exit_code in (ExitCode.FAILED_CONVERT, ExitCode.NO_INPUT), file_path

    @pytest.mark.parametrize(["file_creator", "expected"], [[valid_excel_file_1, ExitCode.SUCCESS]])
    def test_normal_one_file(self, file_creator, expected):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_path = file_creator()
            result = runner.invoke(cmd, ["-o", db_path, "file", file_path])

            assert result.exit_code == expected, file_path

    def test_normal_multi_file_different_table(self):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            files = [
                valid_json_single_file(),
                valid_json_single_b_file(),
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

            result = runner.invoke(cmd, ["-o", db_path, "file"] + files)
            assert result.exit_code == ExitCode.SUCCESS

            con = SimpleSQLite(db_path, "r")
            expected_tables = [
                "singlejson",
                "multij1",
                "multij2",
                "valid_kv",
                "csv_a",
                "rename_insert",
                "excel_sheet_a",
                "excel_sheet_c",
                "excel_sheet_d",
                "valid_ltsv_a",
                "testtitle_tablename",
                "testtitle_html2",
                "tsv_a",
                "valid_mdtable_markdown1",
                "root",
                SourceInfo.get_table_name(),
            ]
            actual_tables = con.fetch_table_names()

            print_test_result(expected=expected_tables, actual=actual_tables)

            assert set(actual_tables) == set(expected_tables)

            expected_data_table = {
                "singlejson": [(1, 4.0, "a"), (2, 2.1, "bb"), (3, 120.9, "ccc")],
                "multij1": [(1, 4.0, "a"), (2, 2.1, "bb"), (3, 120.9, "ccc")],
                "multij2": [(1, 4.0), (2, None), (3, 120.9)],
                "valid_kv": [("json_b", "hoge"), ("json_c", "bar")],
                "csv_a": [(1, 4.0, "a"), (2, 2.1, "bb"), (3, 120.9, "ccc")],
                "rename_insert": [
                    (1, 55, "D Sam", 31, "Raven"),
                    (2, 36, "J Ifdgg", 30, "Raven"),
                    (3, 91, "K Wedfb", 28, "Raven"),
                ],
                "excel_sheet_a": [(1.0, 1.1, "a"), (2.0, 2.2, "bb"), (3.0, 3.3, "cc")],
                "excel_sheet_c": [(1, 1.1, "a"), (2, "", "bb"), (3, 3.3, "")],
                "excel_sheet_d": [(1, 1.1, "a"), (2, "", "bb"), (3, 3.3, "")],
                "testtitle_tablename": [(1, 123.1, "a"), (2, 2.2, "bb"), (3, 3.3, "ccc")],
                "valid_ltsv_a": [
                    (1, 123.1, '"ltsv0"', 1.0, '"1"'),
                    (2, 2.2, '"ltsv1"', 2.2, '"2.2"'),
                    (3, 3.3, '"ltsv2"', 3.0, '"cccc"'),
                ],
                "testtitle_html2": [(1, 123.1), (2, 2.2), (3, 3.3)],
                "tsv_a": [(1, 4.0, "tsv0"), (2, 2.1, "tsv1"), (3, 120.9, "tsv2")],
                "valid_mdtable_markdown1": [(1, 123.1, "a"), (2, 2.2, "bb"), (3, 3.3, "ccc")],
            }
            for table in con.fetch_table_names():
                if table in (SourceInfo.get_table_name(), "root"):
                    continue

                result = con.select("*", table_name=table)
                expected_data = expected_data_table.get(table)
                actual_data = result.fetchall()

                message = "table={}, expected={}, actual={}".format(
                    table, expected_data, actual_data
                )

                print("--- table: {} ---".format(table))
                print_test_result(expected=expected_data, actual=actual_data)

                assert sorted(expected_data) == sorted(actual_data), message

    def test_normal_format_ssv(self):
        db_path = "test_ssv.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_path = valid_ssv_file()
            result = runner.invoke(cmd, ["-o", db_path, "file", file_path, "--format", "ssv"])
            print_traceback(result)

            assert result.exit_code == ExitCode.SUCCESS

            con = SimpleSQLite(db_path, "r")
            data = con.select_as_tabledata(table_name="ssv")
            expected = (
                "table_name=ssv, "
                "headers=[USER, PID, %CPU, %MEM, VSZ, RSS, TTY, STAT, START, TIME, COMMAND], "
                "cols=11, rows=5"
            )

            assert str(data) == expected

    @pytest.mark.parametrize(
        ["file_creator", "index_list", "expected"],
        [
            [
                valid_csv_file_3_1,
                "aa,ac",
                dedent(
                    """\
                    .. table:: valid_csv_3_1

                        +-----+-------+----+---+-------+-----+-----+
                        |Field| Type  |Null|Key|Default|Index|Extra|
                        +=====+=======+====+===+=======+=====+=====+
                        |aa   |REAL   |YES |   |NULL   |  X  |     |
                        +-----+-------+----+---+-------+-----+-----+
                        |ab   |INTEGER|YES |   |NULL   |     |     |
                        +-----+-------+----+---+-------+-----+-----+
                        |ac   |TEXT   |YES |   |NULL   |  X  |     |
                        +-----+-------+----+---+-------+-----+-----+
                    """
                ),
            ]
        ],
    )
    def test_normal_index(self, file_creator, index_list, expected):
        db_path = "test_index.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_path = file_creator()
            result = runner.invoke(cmd, ["-o", db_path, "--index", index_list, "file", file_path])
            print_traceback(result)
            assert result.exit_code == ExitCode.SUCCESS

            extractor = SQLiteSchemaExtractor(db_path)
            output = extractor.fetch_table_schema("valid_csv_3_1").dumps()
            print_test_result(expected=expected, actual=output)
            assert output == expected

    def test_normal_dup_col_csv_file(self):
        db_path = "test_dup_col.sqlite"
        runner = CliRunner()
        expected = dedent(
            """\
            _source_info_ (source_id, dir_name, base_name, format, dst_table, size, mtime)
            dup_col (A, A_2, A_1)"""
        )

        with runner.isolated_filesystem():
            result = runner.invoke(cmd, ["-o", db_path, "file", dup_col_csv_file()])
            print_traceback(result)
            assert result.exit_code == ExitCode.SUCCESS

            extractor = SQLiteSchemaExtractor(db_path)
            options = {"output_format": "text", "verbosity_level": 1}
            print_test_result(expected=expected, actual=extractor.dumps(**options))
            assert len(extractor.dumps(**options)) > 100

    def test_normal_symbols_attr(self):
        db_path = "test_symbols_attr.sqlite"
        runner = CliRunner()
        expected = dedent("symbols_attr (A1_A, B2B, C3_C)")

        with runner.isolated_filesystem():
            result = runner.invoke(
                cmd, ["-o", db_path, "--replace-symbol", "_", "file", symbols_attr_csv_file()]
            )
            print_traceback(result)
            assert result.exit_code == ExitCode.SUCCESS

            extractor = SQLiteSchemaExtractor(db_path)
            options = {"output_format": "text", "verbosity_level": 1}
            schema = extractor.fetch_table_schema("symbols_attr")
            print_test_result(expected=expected, actual=schema.dumps(**options))
            assert schema.dumps(**options) == expected

    def test_normal_append(self):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            files = [valid_json_multi_file_2_1()]
            table_name = "multij2"
            expected_tables = [table_name, SourceInfo.get_table_name()]

            # first execution without --append option (new) ---
            result = runner.invoke(cmd, ["-o", db_path, "file"] + files)
            print_traceback(result)
            assert result.exit_code == ExitCode.SUCCESS

            con = SimpleSQLite(db_path, "r")

            actual_tables = con.fetch_table_names()

            print_test_result(expected=expected_tables, actual=actual_tables)

            assert set(actual_tables) == set(expected_tables)

            actual_data = con.select("*", table_name=table_name).fetchall()
            expected_data = [(1, 4.0, "a"), (2, 2.1, "bb"), (3, 120.9, "ccc")]

            print_test_result(expected=expected_data, actual=actual_data)

            assert expected_data == actual_data

            # second execution with --append option ---
            result = runner.invoke(cmd, ["-o", db_path, "--append", "file"] + files)
            print_traceback(result)
            assert result.exit_code == ExitCode.SUCCESS

            con = SimpleSQLite(db_path, "r")

            actual_tables = con.fetch_table_names()

            print_test_result(expected=expected_tables, actual=actual_tables)

            assert set(actual_tables) == set(expected_tables)

            actual_data = con.select("*", table_name=table_name).fetchall()
            expected_data = [
                (1, 4.0, "a"),
                (2, 2.1, "bb"),
                (3, 120.9, "ccc"),
                (1, 4.0, "a"),
                (2, 2.1, "bb"),
                (3, 120.9, "ccc"),
            ]

            print_test_result(expected=expected_data, actual=actual_data)

            assert expected_data == actual_data

            # third execution without --append option (overwrite) ---
            result = runner.invoke(cmd, ["-o", db_path, "file"] + files)
            print_traceback(result)
            assert result.exit_code == ExitCode.SUCCESS

            con = SimpleSQLite(db_path, "r")

            actual_tables = con.fetch_table_names()

            print_test_result(expected=expected_tables, actual=actual_tables)

            assert set(actual_tables) == set(expected_tables)

            actual_data = con.select("*", table_name=table_name).fetchall()
            expected_data = [(1, 4.0, "a"), (2, 2.1, "bb"), (3, 120.9, "ccc")]

            print_test_result(expected=expected_data, actual=actual_data)

            assert expected_data == actual_data

    def test_normal_multi_file_same_table_same_structure(self):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            files = [valid_json_multi_file_2_1(), valid_json_multi_file_2_2()]

            result = runner.invoke(cmd, ["-o", db_path, "file"] + files)
            print_traceback(result)
            assert result.exit_code == ExitCode.SUCCESS

            con = SimpleSQLite(db_path, "r")
            expected_tables = ["multij2", SourceInfo.get_table_name()]
            actual_tables = con.fetch_table_names()

            print_test_result(expected=expected_tables, actual=actual_tables)

            assert set(actual_tables) == set(expected_tables)

            expected_data_table = {
                "multij2": [
                    (1, 4.0, "a"),
                    (2, 2.1, "bb"),
                    (3, 120.9, "ccc"),
                    (1, 4.0, "a"),
                    (2, 2.1, "bb"),
                    (3, 120.9, "ccc"),
                ]
            }

            for table in con.fetch_table_names():
                if table == SourceInfo.get_table_name():
                    continue

                expected_data = expected_data_table.get(table)
                actual_data = con.select("*", table_name=table).fetchall()

                message = "table={}, expected={}, actual={}".format(
                    table, expected_data, actual_data
                )

                print("--- table: {} ---".format(table))
                print_test_result(expected=expected_data, actual=actual_data)

                assert expected_data == actual_data, message

    def test_normal_multi_file_same_table_different_structure(self):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            files = [valid_json_multi_file_2_2(), valid_json_multi_file_2_3()]

            result = runner.invoke(cmd, ["-o", db_path, "file"] + files)
            print_traceback(result)
            assert result.exit_code == ExitCode.SUCCESS

            con = SimpleSQLite(db_path, "r")
            expected_tables = ["multij2", "multij2_1", SourceInfo.get_table_name()]
            actual_tables = con.fetch_table_names()

            print_test_result(expected=expected_tables, actual=actual_tables)

            assert set(actual_tables) == set(expected_tables)

            expected_data_table = {
                "multij2": [(1, 4.0, "a"), (2, 2.1, "bb"), (3, 120.9, "ccc")],
                "multij2_1": [("abc", "a", 4.0), ("abc", "bb", 2.1), ("abc", "ccc", 120.9)],
            }

            for table in con.fetch_table_names():
                if table == SourceInfo.get_table_name():
                    continue

                expected_data = expected_data_table.get(table)
                actual_data = con.select("*", table_name=table).fetchall()

                message = "table={}, expected={}, actual={}".format(
                    table, expected_data, actual_data
                )

                print("--- table: {} ---".format(table))
                print_test_result(expected=expected_data, actual=actual_data)

                assert actual_data == expected_data, message

    def test_normal_complex_json(self):
        db_path = "test_complex_json.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_path = valid_complex_json_file()
            result = runner.invoke(cmd, ["-o", db_path, "file", file_path])
            print_traceback(result)

            assert result.exit_code == ExitCode.SUCCESS

            con = SimpleSQLite(db_path, "r")
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

    def test_normal_not_exit_file(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(cmd, ["file", "not_exist.csv"])
            print_traceback(result)

            assert result.exit_code == ExitCode.NO_INPUT

    def test_normal_type_hint_header(self):
        runner = CliRunner()
        basename = "type_hint_header"
        file_path = "{}.csv".format(basename)
        db_path = "{}.sqlite".format(basename)

        with runner.isolated_filesystem():
            with open(file_path, "w") as f:
                f.write(
                    dedent(
                        """\
                        "a text","b integer","c real"
                        1,"1","1.1"
                        2,"2","1.2"
                        3,"3","1.3"
                        """
                    )
                )
                f.flush()

            result = runner.invoke(cmd, ["--type-hint-header", "-o", db_path, "file", file_path])
            print_traceback(result)
            assert result.exit_code == ExitCode.SUCCESS

            con = SimpleSQLite(db_path, "r")
            tbldata = con.select_as_tabledata(basename)
            assert tbldata.headers == ["a text", "b integer", "c real"]
            assert tbldata.rows == [("1", 1, 1.1), ("2", 2, 1.2), ("3", 3, 1.3)]

    def test_normal_add_primary_key(self):
        runner = CliRunner()
        basename = "add_primary_key"
        file_path = "{}.csv".format(basename)
        db_path = "{}.sqlite".format(basename)

        with runner.isolated_filesystem():
            with open(file_path, "w") as f:
                f.write(
                    dedent(
                        """\
                        "a","b"
                        11,"xyz"
                        22,"abc"
                        """
                    )
                )
                f.flush()

            result = runner.invoke(
                cmd, ["--add-primary-key", "id", "-o", db_path, "file", file_path]
            )
            print_traceback(result)
            assert result.exit_code == ExitCode.SUCCESS

            con = SimpleSQLite(db_path, "r")
            tbldata = con.select_as_tabledata(basename)
            assert tbldata.headers == ["id", "a", "b"]
            assert tbldata.rows == [(1, 11, "xyz"), (2, 22, "abc")]

    def test_normal_no_type_inference(self):
        runner = CliRunner()
        basename = "no_type_inference"
        file_path = "{}.csv".format(basename)
        db_path = "{}.sqlite".format(basename)

        with runner.isolated_filesystem():
            with open(file_path, "w") as f:
                f.write(
                    dedent(
                        """\
                        "a","b"
                        11,"xyz"
                        22,"abc"
                        """
                    )
                )
                f.flush()

            result = runner.invoke(cmd, ["--no-type-inference", "-o", db_path, "file", file_path])
            print_traceback(result)
            assert result.exit_code == ExitCode.SUCCESS

            con = SimpleSQLite(db_path, "r")
            tbldata = con.select_as_tabledata(basename)
            assert tbldata.headers == ["a", "b"]
            assert tbldata.rows == [("11", "xyz"), ("22", "abc")]
