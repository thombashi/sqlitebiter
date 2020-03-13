"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from enum import Enum, unique


@unique
class Context(Enum):
    DUP_DATABASE = 1
    CONVERT_CONFIG = 5
    INDEX_LIST = 10
    ADD_PRIMARY_KEY_NAME = 15
    TYPE_INFERENCE = 19
    TYPE_HINT_HEADER = 20
    LOG_LEVEL = 30
    OUTPUT_PATH = 40
    VERBOSITY_LEVEL = 50
    SYMBOL_REPLACE_VALUE = 60


@unique
class DupDatabase(Enum):
    OVERWRITE = 1
    APPEND = 2
    SKIP = 3  # TODO
