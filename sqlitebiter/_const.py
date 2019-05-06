# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals


PROGRAM_NAME = "sqlitebiter"
MAX_VERBOSITY_LEVEL = 2

IPYNB_FORMAT_NAME_LIST = ["ipynb"]
TABLE_NOT_FOUND_MSG_FORMAT = "convertible table not found in {}"


class ExitCode(object):
    SUCCESS = 0
    FAILED_LOADER_NOT_FOUND = 1
    FAILED_CONVERT = 2
    FAILED_HTTP = 3
    NO_INPUT = 10
