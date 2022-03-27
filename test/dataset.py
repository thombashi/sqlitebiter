"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from textwrap import dedent

import path
import xlsxwriter


def valid_json_single_file():
    file_path = "singlejson.json"
    with open(file_path, "w") as f:
        f.write(dedent("""\
            [
                {"attr_b": 4, "attr_c": "a", "attr_a": 1},
                {"attr_b": 2.1, "attr_c": "bb", "attr_a": 2},
                {"attr_b": 120.9, "attr_c": "ccc", "attr_a": 3}
            ]"""))

    return file_path


def valid_json_single_b_file():
    file_path = "singlejson_b.json"

    with open(file_path, "w") as f:
        f.write(dedent("""\
            [
                {"attr_b": 4, "attr_c": "a", "attr_a": [1]},
                {"attr_b": 2.1, "attr_c": "bb", "attr_a": [2]},
                {"attr_b": 120.9, "attr_c": "ccc", "attr_a": [3]}
            ]"""))

    return file_path


def valid_json_multi_file_1():
    file_path = "multijson.json"

    with open(file_path, "w") as f:
        f.write(dedent("""\
            {
                "multij1" : [
                    {"attr_b": 4, "attr_c": "a", "attr_a": 1},
                    {"attr_b": 2.1, "attr_c": "bb", "attr_a": 2},
                    {"attr_b": 120.9, "attr_c": "ccc", "attr_a": 3}
                ],
                "multij2" : [
                    {"a": 1, "b": 4},
                    {"a": 2 },
                    {"a": 3, "b": 120.9}
                ],
                "2018Asset": [
                    {
                        "RANK": "1",
                        "id": "item_entertainment_18_212",
                        "count": "1billion"
                    }
                ]
            }"""))

    return file_path


def valid_json_multi_file_2_1():
    file_path = "multijson_2_1.json"

    with open(file_path, "w") as f:
        f.write(dedent("""\
            {
                "multij2" : [
                    {"attr_b": 4, "attr_c": "a", "attr_a": 1},
                    {"attr_b": 2.1, "attr_c": "bb", "attr_a": 2},
                    {"attr_b": 120.9, "attr_c": "ccc", "attr_a": 3}
                ]
            }"""))

    return file_path


def valid_json_multi_file_2_2():
    file_path = "multijson_2_2.json"

    with open(file_path, "w") as f:
        f.write(dedent("""\
            {
                "multij2" : [
                    {"attr_b": 4, "attr_c": "a", "attr_a": 1},
                    {"attr_b": 2.1, "attr_c": "bb", "attr_a": 2},
                    {"attr_b": 120.9, "attr_c": "ccc", "attr_a": 3}
                ]
            }"""))

    return file_path


def valid_json_multi_file_2_3():
    file_path = "multijson_2_3.json"

    with open(file_path, "w") as f:
        f.write(dedent("""\
            {
                "multij2" : [
                    {"attr_b": "a", "attr_c": 4, "attr_a": "abc"},
                    {"attr_b": "bb", "attr_c": 2.1, "attr_a": "abc"},
                    {"attr_b": "ccc", "attr_c": 120.9, "attr_a": "abc"}
                ]
            }"""))

    return file_path


def valid_json_symbols():
    file_path = "symbols.json"

    with open(file_path, "w") as f:
        f.write(dedent("""\
            {
                "comp" : [
                    {"ABCD>8.5": "aaa", "ABCD<8.5": 0},
                    {"ABCD>8.5": "bbb", "ABCD<8.5": 9}
                ],
                "symbols": [
                    {
                        "a!bc#d$e%f&gh(i)j": "aaa",
                        "k@l[m]n{o}p;q:r,s.t/u": 1
                    }
                ]
            }"""))

    return file_path


def valid_json_kv_file():
    file_path = "valid_kv.json"

    with open(file_path, "w") as f:
        f.write("""{
            "json_b" : "hoge",
            "json_c" : "bar"
        }""")

    return file_path


def valid_jsonlines_file():
    file_path = "valid_jsonlines.ldjson"

    with open(file_path, "w") as f:
        f.write(dedent("""\
            {"attr_a": "1", "attr_b": "4", "attr_c": "a"}
            {"attr_b": "2.1", "attr_c": "bb", "attr_a": "2"}
            {"attr_b": "120.9", "attr_c": "ccc", "attr_a": "3"}
        """))

    return file_path


def valid_csv_file_1_1():
    file_path = "csv_a.csv"
    with open(file_path, "w") as f:
        f.write("\n".join([
            '"attr_a","attr_b","attr_c"',
            '1,4,"a"',
            '2,2.1,"bb"',
            '3,120.9,"ccc"',
        ]))

    return file_path


def valid_csv_file_1_2():
    file_path = "csv_a.csv"
    with open(file_path, "w") as f:
        f.write("\n".join([
            '"attr_a","attr_b","attr_c"',
            '4,1,"a"',
            '2.1,2,"bb"',
            '120.9,3,"ccc"',
        ]))

    return file_path


def valid_csv_file_2_1():
    # filename that include a reserved keyword of SQLite
    file_path = "insert.csv"

    with open(file_path, "w") as f:
        f.write("\n".join([
            "index,No,Player_last_name,Age,Team",
            "1, 55,D Sam, 31,Raven",
            "2, 36,J Ifdgg, 30,Raven",
            "3, 91,K Wedfb, 28,Raven",
        ]))

    return file_path


def valid_csv_file_3_1():
    file_path = "valid_csv_3_1.csv"
    with open(file_path, "w") as f:
        f.write("\n".join([
            '"aa","ab","ac"',
            '4,1,"a"',
            '2.1,2,"bb"',
            '120.9,3,"ccc"',
        ]))

    return file_path


def dup_col_csv_file():
    file_path = "dup_col.csv"
    with open(file_path, "w") as f:
        f.write("\n".join([
            '"A","A","A_1"',
            '4,1,"a"',
            '2.1,2,"bb"',
            '120.9,3,"ccc"',
        ]))

    return file_path


def symbols_attr_csv_file():
    file_path = "symbols_attr.csv"
    with open(file_path, "w") as f:
        f.write("\n".join([
            '"A1-!A","#B2B$","C3@C==^"',
            '4,1,"a"',
            '2.1,2,"bb"',
        ]))

    return file_path


def invalid_csv_file():
    file_path = "invalid_csv.csv"

    with open(file_path, "w") as f:
        f.write("\n".join([
            '"attr_a"\t"attr_b"\t"attr_c"',
            '1\t4\t"tsv0"',
            '2\t2.1\t"tsv1"',
            '3\t120.9\t"tsv2"',
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


def invalid_tsv_file():
    file_path = "invalid_tsv.tsv"

    with open(file_path, "w") as f:
        f.write("\n".join([
            '"attr_a","attr_b","attr_c"',
            '1,4,"a"',
            '2,2.1,"bb"',
            '3,120.9,"ccc"',
        ]))

    return file_path


def valid_ssv_file():
    file_path = "ssv.txt"
    with open(file_path, "w") as f:
        f.write(dedent("""\
            USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
            root         1  0.0  0.4  77664  8784 ?        Ss   May11   0:02 /sbin/init
            root         2  0.0  0.0      0     0 ?        S    May11   0:00 [kthreadd]
            root         4  0.0  0.0      0     0 ?        I<   May11   0:00 [kworker/0:0H]
            root         6  0.0  0.0      0     0 ?        I<   May11   0:00 [mm_percpu_wq]
            root         7  0.0  0.0      0     0 ?        S    May11   0:01 [ksoftirqd/0]
        """))

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


def valid_excel_file_1():
    file_path = "valid_underscore.xlsx"
    workbook = xlsxwriter.Workbook(str(file_path))

    worksheet = workbook.add_worksheet("sheet_a")
    table = [
        ["data", "_data", "da_ta", "data_"],
        [1, 0.0, "a", "aaaa"],
        [2, 0.1, "b", "bbbb"],
        [3, 0.2, "c", "cccc"],
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
        f.write(dedent("""\
            <title>testtitle</title>
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
            """))

    return file_path


def valid_uneven_html_file():
    file_path = "valid_uneven.html"

    with open(file_path, "w") as f:
        f.write(dedent("""\
            <!DOCTYPE html>
            <html>
            <head>
            <meta name="generator" content=
            "HTML Tidy for HTML5 for Linux version 5.6.0">
            <title></title>
            </head>
            <body>
            <table>
            <tbody>
            <tr>
            <td width="125px"><span>Vincolo [10021]</span></td>
            <td><strong>PARCO DELLA VILLA SCHELLA CON VEGETAZIONE ULTRASECOLARE
            NEL COMUNE DI OVADA</strong></td>
            </tr>
            <tr>
            <td>Pubblicazione</td>
            <td>*</td>
            </tr>
            <tr>
            <td>Decreto</td>
            <td>emissione: 1964-10-05, notifica: 1964-10-20, trascrizione:
            1965-01-04</td>
            </tr>
            <tr>
            <td>Legge istitutiva</td>
            <td>L1497/39</td>
            </tr>
            <tr>
            <td>Stato del vincolo</td>
            <td>Vincolo operante</td>
            </tr>
            <tr>
            <td>Uso</td>
            <td>Modificabilità previa autorizzazione</td>
            </tr>
            <tr>
            <td>Lettera M</td>
            <td>NO</td>
            </tr>
            <tr>
            <td><span>Geometria</span></td>
            </tr>
            </tbody>
            </table>
            </body>
            </html>
            """))

    return file_path


def invalid_html_file():
    file_path = "invalid_html.html"

    with open(file_path, "w") as f:
        f.write(dedent("""\
            <html>
            <head>
                header
            </head>
            <body>
                hogehoge
            </body>
            </html>
            """))

    return file_path


def valid_ltsv_file():
    file_path = "valid_ltsv_a.ltsv"

    with open(file_path, "w") as f:
        f.write(dedent("""\
            a.0:1\tb-1:123.1\tc_2:"ltsv0"\t"dd":1.0\te.f-g_4:"1"
            a.0:2\tb-1:2.2\tc_2:"ltsv1"\t"dd":2.2\te.f-g_4:"2.2"
            a.0:3\tb-1:3.3\tc_2:"ltsv2"\t"dd":3.0\te.f-g_4:"cccc"
            """))

    return file_path


def invalid_ltsv_file():
    file_path = "invalid_ltsv.ltsv"

    with open(file_path, "w") as f:
        f.write("\n".join([
            '"attr_a"\t"attr_b"\t"attr_c"',
            '1\t4\t"tsv0"',
            '2\t2.1\t"tsv1"',
            '3\t120.9\t"tsv2"',
        ]))

    return file_path


def valid_markdown_file():
    file_path = "valid_mdtable.md"

    with open(file_path, "w") as f:
        f.write(dedent("""\
            | a |  b  | c |
            |--:|----:|---|
            |  1|123.1|a  |
            |  2|  2.2|bb |
            |  3|  3.3|ccc|
            """))

    return file_path


def valid_utf8_csv_file():
    encoding = "utf8"
    file_path = f"valid_{encoding:s}.csv"

    with open(file_path, "w", encoding=encoding) as f:
        f.write(dedent("""\
            "姓","名","生年月日","郵便番号","住所","電話番号"
            "山田","太郎","2001/1/1","100-0002","東京都千代田区皇居外苑","03-1234-5678"
            "山田","次郎","2001/1/2","251-0036","神奈川県藤沢市江の島１丁目","03-9999-9999"
            """))

    return file_path


def valid_utf16_csv_file():
    encoding = "utf16"
    file_path = f"valid_{encoding:s}.csv"

    with open(file_path, "w", encoding=encoding) as f:
        f.write(dedent("""\
            "姓","名","生年月日","郵便番号","住所","電話番号"
            "山田","太郎","2001/1/1","100-0002","東京都千代田区皇居外苑","03-1234-5678"
            "山田","次郎","2001/1/2","251-0036","神奈川県藤沢市江の島１丁目","03-9999-9999"
            """))

    return file_path


def not_supported_format_file():
    file_path = "invalid_format.txt"

    with open(file_path, "w") as f:
        f.write("invalid format")

    return file_path


complex_json = dedent("""\
    {
        "name": "Zendesk Chat",
        "slug": "zopim-live-chat",
        "version": "1.4.12",
        "author": "<a href=http: //www.zendesk.com/chat?iref=wp_plugin>Zendesk",
        "author_profile": "https://profiles.wordpress.org/bencxr",
        "requires": "3.1",
        "tested": "4.7.10",
        "requires_php": false,
        "compatibility": [],
        "rating": 80,
        "ratings": {
            "5": 18,
            "4": 1,
            "3": 2,
            "2": 1,
            "1": 5
        },
        "num_ratings": 27,
        "support_threads": 1,
        "support_threads_resolved": 0,
        "downloaded": 925716,
        "last_updated": "2017-12-01 6:22am GMT",
        "added": "2010-01-20",
        "homepage": "http://www.zendesk.com/chat?iref=wp_plugin",
        "short_description": "Zendesk Chat (previously Zopim) lets you monitor and chat with visitors surfing your store in real-time. Impress them personally and ease them into th …",
        "download_link": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.4.12.zip",
        "screenshots": {
            "4": {
                "src": "https://ps.w.org/zopim-live-chat/trunk/screenshot-4.png?rev=1779235",
                "caption": "Dashboard View - Open new browser tab"
            },
            "3": {
                "src": "https://ps.w.org/zopim-live-chat/trunk/screenshot-3.png?rev=1779235",
                "caption": "Account Configuration - Linked Up with Launch Dashboard"
            },
            "5": {
                "src": "https://ps.w.org/zopim-live-chat/trunk/screenshot-5.png?rev=1779235",
                "caption": "Widget Customization from Dashboard"
            },
            "1": {
                "src": "https://ps.w.org/zopim-live-chat/trunk/screenshot-1.png?rev=1779235",
                "caption": "Chat window on your website - active chat"
            },
            "2": {
                "src": "https://ps.w.org/zopim-live-chat/trunk/screenshot-2.png?rev=1779235",
                "caption": "Account Configuration - Link Up"
            }
        },
        "tags": {
            "chat": "chat",
            "chat-online": "chat online",
            "contact-plugin": "contact plugin",
            "contact-us": "contact us",
            "customer-support": "customer support"
        },
        "versions": {
            "0.6.1": "https://downloads.wordpress.org/plugin/zopim-live-chat.0.6.1.zip",
            "0.7": "https://downloads.wordpress.org/plugin/zopim-live-chat.0.7.zip",
            "1.0": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.0.zip",
            "1.0.1": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.0.1.zip",
            "1.0.2": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.0.2.zip",
            "1.0.3": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.0.3.zip",
            "1.0.4": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.0.4.zip",
            "1.0.5": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.0.5.zip",
            "1.0.6": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.0.6.zip",
            "1.0.7": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.0.7.zip",
            "1.1.0": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.1.0.zip",
            "1.1.1": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.1.1.zip",
            "1.1.2": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.1.2.zip",
            "1.1.3": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.1.3.zip",
            "1.2.0": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.2.0.zip",
            "1.2.1": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.2.1.zip",
            "1.2.2": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.2.2.zip",
            "1.2.5": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.2.5.zip",
            "1.2.6": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.2.6.zip",
            "1.2.7": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.2.7.zip",
            "1.2.8": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.2.8.zip",
            "1.2.9": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.2.9.zip",
            "1.3.0": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.3.0.zip",
            "1.3.1": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.3.1.zip",
            "1.3.2": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.3.2.zip",
            "1.3.3": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.3.3.zip",
            "1.3.4": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.3.4.zip",
            "1.3.5": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.3.5.zip",
            "1.3.6": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.3.6.zip",
            "1.3.7": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.3.7.zip",
            "1.3.8": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.3.8.zip",
            "1.3.9": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.3.9.zip",
            "1.4.0": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.4.0.zip",
            "1.4.1": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.4.1.zip",
            "1.4.10": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.4.10.zip",
            "1.4.11": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.4.11.zip",
            "1.4.12": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.4.12.zip",
            "1.4.2": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.4.2.zip",
            "1.4.3": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.4.3.zip",
            "1.4.4": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.4.4.zip",
            "1.4.5": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.4.5.zip",
            "1.4.6": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.4.6.zip",
            "1.4.7": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.4.7.zip",
            "1.4.8": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.4.8.zip",
            "1.4.9": "https://downloads.wordpress.org/plugin/zopim-live-chat.1.4.9.zip",
            "trunk": "https://downloads.wordpress.org/plugin/zopim-live-chat.zip"
        },
        "donate_link": ""
    }""")


def valid_complex_json_file():
    file_path = "valid_complex_json.json"

    with open(file_path, "w", encoding="utf8") as f:
        f.write(complex_json)

    return file_path
