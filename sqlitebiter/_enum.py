# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

from enum import Enum, auto


class Context(Enum):
    CREATE_DATABASE = auto()
    CONNECTION = auto()
    INDEX_LIST = auto()
    LOG_LEVEL = auto()
    VERBOSITY_LEVEL = auto()


class ExitCode(object):
    SUCCESS = 0
    FAILED_LOADER_NOT_FOUND = 1
    FAILED_CONVERT = 2
    FAILED_HTTP = 3
    NO_INPUT = 10
