# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import


class ResultCounter(object):

    def __init__(self):
        self.__success_count = 0
        self.__fail_count = 0

    def inc_success(self):
        self.__success_count += 1

    def inc_fail(self):
        self.__fail_count += 1

    def get_return_code(self):
        if self.__success_count > 0:
            return 0

        if self.__fail_count > 0:
            return 1

        return 2
