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

_to_type_hint = {
    "integer": Integer,
    "int": Integer,
    "real": RealNumber,
    "float": RealNumber,
    "str": String,
    "text": String,
}


def normalize_type_hint(type_hint_str):
    return _to_type_hint[type_hint_str.strip().lower()]
