#!/usr/bin/env python3

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import multiprocessing

from sqlitebiter.sqlitebiter import cmd


if __name__ == "__main__":
    multiprocessing.freeze_support()
    cmd()
