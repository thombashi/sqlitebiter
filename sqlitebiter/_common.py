"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""


from typing import Union

from path import Path
from sqliteschema import SQLiteSchemaExtractor

from ._clrm import bright, cyan, green
from ._counter import ResultCounter


DEFAULT_DUP_COL_HANDLER = "rename"


class ResultLogger:
    @property
    def verbosity_level(self) -> int:
        return self.__verbosity_level

    def __init__(
        self,
        logger,
        schema_extractor: SQLiteSchemaExtractor,
        result_counter: ResultCounter,
        verbosity_level: int,
    ) -> None:
        self.__logger = logger
        self.__schema_extractor = schema_extractor
        self.__result_counter = result_counter
        self.__verbosity_level = verbosity_level

    def logging_success(
        self, source: Union[str, Path], table_name: str, is_create_table: bool
    ) -> None:
        table_schema = self.__schema_extractor.fetch_table_schema(table_name.strip())

        self.__result_counter.inc_success(is_create_table)
        self.__logger.info(
            "convert '{source:s}' to '{table_info:s}' table".format(
                source=cyan(source),
                table_info=bright(
                    green(
                        table_schema.dumps(
                            output_format="text", verbosity_level=self.__verbosity_level
                        )
                    )
                ),
            )
        )
