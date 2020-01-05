# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import print_function

import os
import platform

import pytest
from click.testing import CliRunner

from sqlitebiter._const import ExitCode
from sqlitebiter.sqlitebiter import cmd

from .common import print_traceback


db_path = "test.sqlite"


class Test_file_subcommand_ipynb(object):
    IPYNB_FILE_LIST = [
        "test/data/pytablewriter_examples.ipynb",
        "test/data/jupyter_notebook_example.ipynb",
        "test/data/empty.ipynb",
    ]

    @pytest.mark.parametrize(
        ["file_path", "expected"],
        [
            [IPYNB_FILE_LIST[0], ExitCode.SUCCESS],
            [IPYNB_FILE_LIST[1], ExitCode.SUCCESS],
            [IPYNB_FILE_LIST[2], ExitCode.SUCCESS],
        ],
    )
    def test_smoke_one_file(self, file_path, expected):
        runner = CliRunner()

        try:
            result = runner.invoke(cmd, ["-o", db_path, "file", file_path])
            print_traceback(result)

            assert result.exit_code == expected, file_path
        finally:
            if platform.system() != "Windows":
                # avoid a test execution error on AppVeyor
                os.remove(db_path)

    def test_smoke_multi_file(self):
        runner = CliRunner()

        try:
            result = runner.invoke(cmd, ["-o", db_path, "file"] + self.IPYNB_FILE_LIST)
            print_traceback(result)

            assert result.exit_code == ExitCode.SUCCESS
        finally:
            if platform.system() != "Windows":
                # avoid a test execution error on AppVeyor
                os.remove(db_path)

    @pytest.mark.parametrize(
        ["content", "expected"], [["", ExitCode.NO_INPUT], ["{}", ExitCode.NO_INPUT]]
    )
    def test_abnormal_empty_file(self, content, expected):
        runner = CliRunner()

        with runner.isolated_filesystem():
            file_path = "empty.ipynb"

            with open(file_path, "w") as f:
                f.write(content)

            result = runner.invoke(cmd, ["-o", db_path, "file", file_path])
            print_traceback(result)

            assert result.exit_code == expected, file_path
