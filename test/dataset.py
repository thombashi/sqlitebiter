# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import unicode_literals
from __future__ import print_function
import io

import path
import xlsxwriter


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


def valid_csv_file_1():
    file_path = "csv_a.csv"
    with open(file_path, "w") as f:
        f.write("\n".join([
            '"attr_a","attr_b","attr_c"',
            '1,4,"a"',
            '2,2.1,"bb"',
            '3,120.9,"ccc"',
        ]))

    return file_path


def valid_csv_file_2():
    # reserved keywod of SQLite

    file_path = "insert.csv"
    with open(file_path, "w") as f:
        f.write("\n".join([
            "index,No,Player_last_name,Age,Team",
            "1, 55,D Sam, 31,Raven",
            "2, 36,J Ifdgg, 30,Raven",
            "3, 91,K Wedfb, 28,Raven",
        ]))

    return file_path


def valid_tsv_file():
    file_path = "tsv_a.tsv"
    with open(file_path, "w") as f:
        f.write("\n".join([
            '"attr_a"\t"attr_b"\t"attr_c"',
            '1\t4\t"tsv0"',
            '2\t2.1\t"tsv1"',
            '3\t120.9\t"tsv2"',
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


def invalid_excel_file_1():
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


def invalid_excel_file_2():
    file_path = "invalid2.xlsx"
    path.Path(file_path).touch()

    return file_path


def valid_html_file():
    file_path = "htmltable.html"
    with open(file_path, "w") as f:
        f.write("""<title>testtitle</title>
<table id="tablename">
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


def valid_markdown_file():
    file_path = "valid_mdtable.md"
    with open(file_path, "w") as f:
        f.write(""" a |  b  | c 
--:|----:|---
  1|123.1|a  
  2|  2.2|bb 
  3|  3.3|ccc
""")

    return file_path


def valid_multibyte_char_file():
    file_path = "valid_multibyte_char.csv"
    with io.open(file_path, "w", encoding="utf-8") as f:
        f.write(""""姓","名","生年月日","郵便番号","住所","電話番号"
"山田","太郎","2001/1/1","100-0002","東京都千代田区皇居外苑","03-1234-5678"
"山田","次郎","2001/1/2","251-0036","神奈川県藤沢市江の島１丁目","03-9999-9999"
""")

    return file_path


def not_supported_format_file():
    file_path = "invalid_format.txt"
    with open(file_path, "w") as f:
        f.write("invalid format")

    return file_path
