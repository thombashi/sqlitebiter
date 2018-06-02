# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import print_function

import os

import pytest
from click.testing import CliRunner
from sqlitebiter._enum import ExitCode
from sqlitebiter.sqlitebiter import cmd

from .common import print_traceback


db_path = "test.sqlite"


@pytest.mark.xfail
class Test_file_subcommand_ipynb(object):
    IPYNB_FILE_LIST = [
        "test/data/pytablewriter_examples.ipynb",
        "test/data/jupyter_notebook_example.ipynb",
        "test/data/DataProperty.ipynb",
    ]

    @pytest.mark.parametrize(["file_path", "expected"], [
        [IPYNB_FILE_LIST[0], ExitCode.SUCCESS],
        [IPYNB_FILE_LIST[1], ExitCode.SUCCESS],
        [IPYNB_FILE_LIST[2], ExitCode.SUCCESS],
    ])
    def test_smoke_one_file(self, file_path, expected):
        runner = CliRunner()

        try:
            result = runner.invoke(cmd, ["file", file_path, "-o", db_path])
            print_traceback(result)

            assert result.exit_code == expected, file_path
        finally:
            os.remove(db_path)

    def test_smoke_multi_file(self):
        runner = CliRunner()

        try:
            result = runner.invoke(cmd, ["file"] + self.IPYNB_FILE_LIST + ["-o", db_path])
            print_traceback(result)

            assert result.exit_code == ExitCode.SUCCESS
        finally:
            os.remove(db_path)
