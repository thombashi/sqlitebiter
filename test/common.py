"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""


import sys
import traceback


def print_test_result(expected, actual):
    print("[expected]\n{}\n".format(expected))
    print("[actual]\n{}\n".format(actual))


def print_traceback(result):
    traceback.print_tb(result.exc_info[2], file=sys.stdout)
    print("{}\n{}\n".format(result.exc_info[0], result.exc_info[1]))
    print("[output]\n{}".format(result.output))
