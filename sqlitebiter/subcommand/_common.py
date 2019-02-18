# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import re

from typepy import Integer, RealNumber, String


TYPE_HINT_FROM_HEADER_RULES = {
    re.compile("[ -_]text$", re.IGNORECASE): String,
    re.compile("[ -_]integer$", re.IGNORECASE): Integer,
    re.compile("[ -_]real$", re.IGNORECASE): RealNumber,
}
