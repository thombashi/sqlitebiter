"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import re
from typing import Type

from typepy import Integer, RealNumber, String
from typepy.type import AbstractType


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


def normalize_type_hint(type_hint_str: str) -> Type[AbstractType]:
    return _to_type_hint[type_hint_str.strip().casefold()]
