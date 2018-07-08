# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

from enum import Enum


class Context(Enum):
    DUP_TABLE = 1
    INDEX_LIST = 2
    LOG_LEVEL = 3
    OUTPUT_PATH = 4
    VERBOSITY_LEVEL = 5


class ExitCode(object):
    SUCCESS = 0
    FAILED_LOADER_NOT_FOUND = 1
    FAILED_CONVERT = 2
    FAILED_HTTP = 3
    NO_INPUT = 10


class DupTable(Enum):
    OVERWRITE = 1
    APPEND = 2
    SKIP = 3  # TODO
