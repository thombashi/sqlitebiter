"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from enum import Enum, auto, unique


@unique
class Context(Enum):
    DUP_DATABASE = auto()
    CONVERT_CONFIG = auto()
    INDEX_LIST = auto()
    ADD_PRIMARY_KEY_NAME = auto()
    TYPE_INFERENCE = auto()
    TYPE_HINT_HEADER = auto()
    LOG_LEVEL = auto()
    OUTPUT_PATH = auto()
    VERBOSITY_LEVEL = auto()
    MAX_WORKERS = auto()
    SYMBOL_REPLACE_VALUE = auto()


@unique
class DupDatabase(Enum):
    OVERWRITE = auto()
    APPEND = auto()
    SKIP = auto()  # TODO
