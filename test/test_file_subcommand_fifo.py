import os
import platform  # noqa
from concurrent.futures import ProcessPoolExecutor

import pytest
from click.testing import CliRunner
from simplesqlite import SimpleSQLite

from sqlitebiter._const import ExitCode
from sqlitebiter.sqlitebiter import cmd

from .common import print_traceback


def fifo_writer(fifo_name):
    with open(fifo_name, "w") as p:
        p.write(
            r"""{"name": "Stacey Chandler", "address": "5514 Daniel Pines Suite 219\nSouth David, WA 31900"}
            {"name": "Joseph Wright", "address": "037 Laura Turnpike\nMartinezfort, MI 92378"}
            {"name": "Mr. Andrew Gomez", "address": "2605 Martin Spur Suite 854\nRowlandhaven, WY 75523"}
            {"name": "Gina Nguyen", "address": "99522 Pamela Land\nNorth Gabriellaport, TX 07851"}
            {"name": "Erika Fisher", "address": "85239 Brandon Underpass Apt. 798\nNorth Destiny, WA 27159"}
            {"name": "Alicia Thomas", "address": "2103 Weaver Drives Apt. 614\nWest Thomasstad, RI 03345"}
            {"name": "John Williams", "address": "1369 Taylor Island Suite 970\nRamirezstad, GA 24877"}
            {"name": "Emily Fitzgerald", "address": "11086 Juan Hill\nLake Marthaburgh, ME 35035"}
            """
        )
        p.flush()


class Test_sqlitebiter_file:
    @pytest.mark.skipif("platform.system() == 'Windows'")
    def test_smoke_one_file(self):
        db_path = "test.sqlite"
        runner = CliRunner()

        with runner.isolated_filesystem():
            fifo_name = "jsonl_fifo"

            os.mkfifo(fifo_name)

            with ProcessPoolExecutor() as executor:
                executor.submit(fifo_writer, fifo_name)
                result = runner.invoke(cmd, ["-o", db_path, "file", fifo_name, "--format", "jsonl"])

            print_traceback(result)

            assert result.exit_code == ExitCode.SUCCESS, fifo_name

            assert SimpleSQLite(db_path).fetch_num_records("jsonl_fifo") == 8
