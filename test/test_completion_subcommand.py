# encoding: utf-8

from __future__ import print_function

import re

import pytest
from click.testing import CliRunner

from sqlitebiter._const import ExitCode
from sqlitebiter.sqlitebiter import cmd

from .common import print_test_result, print_traceback


class Test_sqlitebiter_completion(object):
    @pytest.mark.parametrize(
        ["shell", "expected"], [["bash", ExitCode.SUCCESS], ["zsh", ExitCode.SUCCESS]]
    )
    def test_smoke(self, shell, expected):
        runner = CliRunner()
        result = runner.invoke(cmd, ["completion", shell])

        print_test_result(expected=result.output, actual=result.output)
        print_traceback(result)

        assert result.exit_code == expected
        assert re.search(re.escape("_sqlitebiter_completion() {"), result.output)
