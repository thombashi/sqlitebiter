# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""


import click
from click.testing import CliRunner
import path
import pytest
import simplesqlite
import xlsxwriter

from sqlitebiter.sqlitebiter import cmd


def valid_json_single_file():
    file_path = "singlejson.json"
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
    file_path = "multijson.json"
    with open(file_path, "w") as f:
        f.write("""{
            "table1" : [
                {"attr_b": 4, "attr_c": "a", "attr_a": 1},
                {"attr_b": 2.1, "attr_c": "bb", "attr_a": 2},
                {"attr_b": 120.9, "attr_c": "ccc", "attr_a": 3}
            ],
            "table2" : [
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


def invalid_excel_file2():
    file_path = "invalid2.xlsx"
    path.Path(file_path).touch()

    return file_path


def valid_html_file():
    file_path = "htmltable.html"
    with open(file_path, "w") as f:
        f.write("""<table id="tablename">
    <caption>caption</caption>
    <tr>
      <th>a</th>
      <th>b</th>
      <th>c</th>
    </tr>
    <tr>
      <td align="right">1</td>
      <td align="right">123.1</td>
      <td align="left">a</td>
    </tr>
    <tr>
      <td align="right">2</td>
      <td align="right">2.2</td>
      <td align="left">bb</td>
    </tr>
    <tr>
      <td align="right">3</td>
      <td align="right">3.3</td>
      <td align="left">ccc</td>
    </tr>
</table>
<table>
    <tr>
      <th>a</th>
      <th>b</th>
    </tr>
    <tr>
      <td align="right">1</td>
      <td align="right">123.1</td>
    </tr>
    <tr>
      <td align="right">2</td>
      <td align="right">2.2</td>
    </tr>
    <tr>
      <td align="right">3</td>
      <td align="right">3.3</td>
    </tr>
</table>
""")

    return file_path


def invalid_html_file():
    file_path = "invalid_html.html"
    with open(file_path, "w") as f:
        f.write("""<html>
  <head>
    header
  </head>
  <body>
    hogehoge
  </body>
</html>
""")

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
            file_list = [
                valid_json_single_file(),
                invalid_json_single_file(),

                valid_json_multi_file(),
                invalid_json_multi_file(),

                csv_file(),

                valid_excel_file(),
                invalid_excel_file(),
                invalid_excel_file2(),

                valid_html_file(),
                invalid_html_file(),
            ]

            result = runner.invoke(cmd, ["file"] + file_list + ["-o", db_path])
            assert result.exit_code == 0

            con = simplesqlite.SimpleSQLite(db_path, "r")
            expected_tables = [
                'singlejson_json1', 'multijson_table1', 'multijson_table2',
                'csv_a',
                'excel_sheet_a', 'excel_sheet_c', 'excel_sheet_d',
                'htmltable_tablename', 'htmltable_html2',
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
                    [(1, '4'), (2, 'NULL'), (3, '120.9')],
                "csv_a": [(1, 4.0, 'a'), (2, 2.1, 'bb'), (3, 120.9, 'ccc')],
                "excel_sheet_a":
                    [(1.0, 1.1, 'a'), (2.0, 2.2, 'bb'), (3.0, 3.3, 'cc')],
                "excel_sheet_c":
                    [(1.0, '1.1', 'a'), (2.0, '', 'bb'), (3.0, '3.3', '')],
                "excel_sheet_d":
                    [(1.0, '1.1', 'a'), (2.0, '', 'bb'), (3.0, '3.3', '')],
                "htmltable_tablename":
                    [(1, 123.1, 'a'), (2, 2.2, 'bb'), (3, 3.3, 'ccc')],
                "htmltable_html2":
                    [(1, 123.1), (2, 2.2), (3, 3.3)],
            }
            for table in con.get_table_name_list():
                result = con.select("*", table_name=table)
                expected_data = expected_data_table.get(table)
                actual_data = result.fetchall()

                message = "table={}, expected={}, actual={}".format(
                    table, expected_data, actual_data)
                assert expected_data == actual_data, message
