"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import sys
import traceback


def print_test_result(expected, actual):
    print(f"[expected]\n{expected}\n")
    print(f"[actual]\n{actual}\n")


def print_traceback(result):
    traceback.print_tb(result.exc_info[2], file=sys.stdout)
    print(f"{result.exc_info[0]}\n{result.exc_info[1]}\n")
    print(f"[output]\n{result.output}")
