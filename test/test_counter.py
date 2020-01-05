# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import pytest

from sqlitebiter._const import ExitCode
from sqlitebiter._counter import ResultCounter


class Test_ResultCounter(object):
    @pytest.mark.parametrize(
        ["success", "fail", "expected"],
        [
            [0, 0, ExitCode.NO_INPUT],
            [1, 0, ExitCode.SUCCESS],
            [1, 1, ExitCode.SUCCESS],
            [0, 1, ExitCode.FAILED_CONVERT],
        ],
    )
    def test_normal(self, success, fail, expected):
        result_counter = ResultCounter()

        for _i in range(success):
            result_counter.inc_success(True)

        for _i in range(fail):
            result_counter.inc_fail()

        assert result_counter.get_return_code() == expected
