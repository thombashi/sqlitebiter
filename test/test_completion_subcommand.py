# encoding: utf-8

from __future__ import print_function

import re

from click.testing import CliRunner
from sqlitebiter._enum import ExitCode
from sqlitebiter.sqlitebiter import cmd

from .common import print_test_result, print_traceback


class Test_sqlitebiter_completion(object):
    def test_smoke(self):
        runner = CliRunner()
        result = runner.invoke(cmd, ["completion"])

        print_test_result(expected=result.output, actual=result.output)
        print_traceback(result)

        assert result.exit_code == ExitCode.SUCCESS
        assert re.search(re.escape("_sqlitebiter_completion() {"), result.output)
