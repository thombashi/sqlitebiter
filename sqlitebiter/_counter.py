# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

from ._enum import ExitCode


class ResultCounter(object):
    @property
    def success_count(self):
        return self.__success_count

    @property
    def fail_count(self):
        return self.__fail_count

    @property
    def skip_count(self):
        return self.__skip_count

    @property
    def total_count(self):
        return self.success_count + self.fail_count + self.skip_count

    @property
    def created_table_count(self):
        return self.__create_table_count

    def __init__(self):
        self.__create_table_count = 0
        self.__success_count = 0
        self.__fail_count = 0
        self.__skip_count = 0

    def __repr__(self):
        return "results: " + ", ".join(
            [
                "success={:d}".format(self.__success_count),
                "failed={:d}".format(self.__fail_count),
                "skip={:s}".format(self.__skip_count),
                "return_code={:d}".format(self.get_return_code()),
            ]
        )

    def inc_success(self, is_create_table):
        self.__success_count += 1

        if is_create_table:
            self.__create_table_count += 1

    def inc_fail(self):
        self.__fail_count += 1

    def inc_skip(self):
        self.__skip_count += 1

    def get_return_code(self):
        if self.__success_count > 0:
            return ExitCode.SUCCESS

        if self.__fail_count > 0:
            return ExitCode.FAILED_CONVERT

        return ExitCode.NO_INPUT
