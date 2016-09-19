# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import pytest
from sqlitebiter._counter import ResultCounter


class Test_ResultCounter(object):

    @pytest.mark.parametrize(["success", "fail", "expected"], [
        [0, 0, 2],
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 1],
    ])
    def test_normal(self, success, fail, expected):
        result_counter = ResultCounter()

        for _i in range(success):
            result_counter.inc_success()

        for _i in range(fail):
            result_counter.inc_fail()

        assert result_counter.get_return_code() == expected
