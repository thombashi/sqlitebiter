# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""


import click
from click.testing import CliRunner
import pytest
import simplesqlite
import xlsxwriter

from sqlitebiter.sqlitebiter import cmd


def valid_json_single_file():
    file_path = "json_a.json"
    with open(file_path, "w") as f:
        f.write("""[
            {"attr_b": 4, "attr_c": "a", "attr_a": 1},
            {"attr_b": 2.1, "attr_c": "bb", "attr_a": 2},
            {"attr_b": 120.9, "attr_c": "ccc", "attr_a": 3}
        ]""")

    return file_path


def invalid_json_single_file():
    file_path = "invalid_json_a.json"
    with open(file_path, "w") as f:
        f.write("""[
            {"attr_b": 4, "attr_c": "a", "attr_a": [1]},
            {"attr_b": 2.1, "attr_c": "bb", "attr_a": [2]},
            {"attr_b": 120.9, "attr_c": "ccc", "attr_a": [3]}
        ]""")

    return file_path


def valid_json_multi_file():
    file_path = "multi.json"
    with open(file_path, "w") as f:
        f.write("""{
            "json_b" : [
                {"attr_b": 4, "attr_c": "a", "attr_a": 1},
                {"attr_b": 2.1, "attr_c": "bb", "attr_a": 2},
                {"attr_b": 120.9, "attr_c": "ccc", "attr_a": 3}
            ],
            "json_c" : [
                {"a": 1, "b": 4},
                {"a": 2 },
                {"a": 3, "b": 120.9}
            ]
        }""")

    return file_path


def invalid_json_multi_file():
    file_path = "invalid_multi.json"
    with open(file_path, "w") as f:
        f.write("""{
            "json_b" : "hoge",
            "json_c" : "bar"
        }""")

    return file_path


def csv_file():
    file_path = "csv_a.csv"
    with open(file_path, "w") as f:
        f.write("\n".join([
            '"attr_a","attr_b","attr_c"',
            '1,4,"a"',
            '2,2.1,"bb"',
            '3,120.9,"ccc"',
        ]))

    return file_path


def valid_excel_file():
    file_path = "valid.xlsx"
    workbook = xlsxwriter.Workbook(str(file_path))

    worksheet = workbook.add_worksheet("excel_sheet_a")
    table = [
        ["", "", "", ""],
        ["", "a", "b", "c"],
        ["", 1, 1.1, "a"],
        ["", 2, 2.2, "bb"],
        ["", 3, 3.3, "cc"],
    ]
    for row_idx, row in enumerate(table):
        for col_idx, item in enumerate(row):
            worksheet.write(row_idx, col_idx, item)

    worksheet = workbook.add_worksheet("excel_sheet_b")

    worksheet = workbook.add_worksheet("excel_sheet_c")
    table = [
        ["", "", ""],
        ["", "", ""],
        ["a", "b", "c"],
        [1, 1.1, "a"],
        [2, "", "bb"],
        [3, 3.3, ""],
    ]
    for row_idx, row in enumerate(table):
        for col_idx, item in enumerate(row):
            worksheet.write(row_idx, col_idx, item)

    worksheet = workbook.add_worksheet("excel_sheet_d")
    table = [
        ["a'b", 'b"c', "c'd[%]"],
        [1, 1.1, "a"],
        [2, "", "bb"],
        [3, 3.3, ""],
    ]
    for row_idx, row in enumerate(table):
        for col_idx, item in enumerate(row):
            worksheet.write(row_idx, col_idx, item)

    workbook.close()

    return str(file_path)


def invalid_excel_file():
    file_path = "invalid.xlsx"
    workbook = xlsxwriter.Workbook(file_path)

    worksheet = workbook.add_worksheet("testsheet1")
    table = [
        ["", "", "", ""],
        ["", "a", "", "c"],
        ["", "aa", "ab", ""],
        ["", "", 1.1, "a"],
    ]
    for row_idx, row in enumerate(table):
        for col_idx, item in enumerate(row):
            worksheet.write(row_idx, col_idx, item)

    worksheet = workbook.add_worksheet("testsheet2")

    workbook.close()

    return file_path


class Test_sqlitebiter:

    @pytest.mark.parametrize(["option_list", "expected"], [
        [["-h"], 0],
        [["file", "-h"], 0],
        [["gs", "-h"], 0],
    ])
    def test_help(self, option_list, expected):
        runner = CliRunner()
        result = runner.invoke(cmd, option_list)
        assert result.exit_code == 0

    def test_normal(self):
        db_path = "test.sqlite"
        runner = CliRunner()
        with runner.isolated_filesystem():
            file_list = []

            file_list.append(valid_json_single_file())
            file_list.append(invalid_json_single_file())

            file_list.append(valid_json_multi_file())
            file_list.append(invalid_json_multi_file())

            file_list.append(csv_file())

            file_list.append(valid_excel_file())
            file_list.append(invalid_excel_file())

            result = runner.invoke(cmd, ["file"] + file_list + ["-o", db_path])
            assert result.exit_code == 0

            con = simplesqlite.SimpleSQLite(db_path, "r")
            expected_tables = [
                'json_a', 'json_c', 'json_b',
                'csv_a', 'excel_sheet_a', 'excel_sheet_c', 'excel_sheet_d',
            ]

            assert set(con.get_table_name_list()) == set(expected_tables)

            expected_data = {
                "json_a": [(1, 4.0, 'a'), (2, 2.1, 'bb'), (3, 120.9, 'ccc')],
                "json_b": [(1, 4.0, 'a'), (2, 2.1, 'bb'), (3, 120.9, 'ccc')],
                "json_c": [(1, '4'), (2, 'NULL'), (3, '120.9')],
                "csv_a": [(1, 4.0, 'a'), (2, 2.1, 'bb'), (3, 120.9, 'ccc')],
                "excel_sheet_a":
                    [(1.0, 1.1, 'a'), (2.0, 2.2, 'bb'), (3.0, 3.3, 'cc')],
                "excel_sheet_c":
                    [(1.0, '1.1', 'a'), (2.0, '', 'bb'), (3.0, '3.3', '')],
                "excel_sheet_d":
                    [(1.0, '1.1', 'a'), (2.0, '', 'bb'), (3.0, '3.3', '')],
            }
            for table in con.get_table_name_list():
                result = con.select("*", table_name=table)
                assert expected_data.get(table) == result.fetchall()
