#!/usr/bin/env python3

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import multiprocessing

from sqlitebiter.__main__ import cmd


if __name__ == "__main__":
    multiprocessing.freeze_support()
    cmd()
