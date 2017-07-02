# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import


class Context(object):
    IS_APPEND_TABLE = "IS_APPEND_TABLE"
    LOG_LEVEL = "LOG_LEVEL"
    VERBOSITY_LEVEL = "VERBOSITY_LEVEL"


class ExitCode(object):
    SUCCESS = 0
    FAILED_LOADER_NOT_FOUND = 1
    FAILED_CONVERT = 2
    FAILED_HTTP = 3
    NO_INPUT = 10
