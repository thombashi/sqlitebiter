"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import os.path
from textwrap import indent
from typing import Optional, Sequence, Set, Tuple

from path import Path
from pytablereader.interface import AbstractTableReader
from simplesqlite import SimpleSQLite
from simplesqlite.model import Integer, Model, Text
from tabledata import TableData
from tcolorpy import tcolor

from .._common import DEFAULT_DUP_COL_HANDLER, ResultLogger
from .._const import MAX_VERBOSITY_LEVEL, PROGRAM_NAME, TABLE_NOT_FOUND_MSG_FORMAT
from .._counter import ResultCounter
from ._ipynb_converter import convert_nb
from ._table_creator import TableCreator


class SourceInfo(Model):
    source_id = Integer(not_null=True)
    dir_name = Text()
    base_name = Text(not_null=True)
    format_name = Text(not_null=True)
    dst_table = Text(not_null=True)
    size = Integer()
    mtime = Integer()

    def get_name(self, verbosity_level):
        if verbosity_level == 0 or self.dir_name is None:
            return self.base_name

        return os.path.join(self.dir_name, self.base_name)


class TableConverter:
    def __init__(
        self,
        logger,
        con: SimpleSQLite,
        symbol_replace_value: Optional[str],
        add_pri_key_name: Optional[str],
        convert_configs,
        index_list: Sequence[str],
        is_type_inference: bool,
        is_type_hint_header: bool,
        verbosity_level: int,
        max_workers: int,
        format_name=None,
        encoding=None,
    ):
        self._logger = logger
        self._con = con
        self._symbol_replace_value = symbol_replace_value
        self._convert_configs = convert_configs
        self._index_list = index_list
        self._is_type_inference = is_type_inference
        self._is_type_hint_header = is_type_hint_header
        self._verbosity_level = verbosity_level
        self._max_workers = max_workers
        self._format_name = format_name
        self._encoding = encoding

        self._result_counter = ResultCounter()
        self._result_logger = ResultLogger(
            logger, self._con.schema_extractor, self._result_counter, self._verbosity_level
        )
        self._table_creator = TableCreator(
            logger=self._logger,
            dst_con=con,
            add_pri_key_name=add_pri_key_name,
            result_logger=self._result_logger,
            verbosity_level=verbosity_level,
            max_workers=self._max_workers,
        )

        SourceInfo.attach(con, is_hidden=True)
        SourceInfo.create()

    def _fetch_next_source_id(self) -> int:
        source_id = self._con.fetch_value(
            select="MAX({})".format("source_id"), table_name=SourceInfo.get_table_name()
        )

        if source_id is None:
            return 1

        return source_id + 1

    def get_return_code(self) -> int:
        return self._result_counter.get_return_code()

    def get_success_count(self) -> int:
        return self._result_counter.success_count

    def normalize_table(self, table_data: TableData, dup_col_handler=None) -> TableData:
        from pathvalidate import replace_symbol, replace_unprintable_char
        from simplesqlite import SQLiteTableDataSanitizer

        if dup_col_handler is None:
            dup_col_handler = DEFAULT_DUP_COL_HANDLER

        normalized_table_data = SQLiteTableDataSanitizer(
            table_data,
            dup_col_handler=dup_col_handler,
            is_type_inference=self._is_type_inference,
            max_workers=self._max_workers,
        ).normalize()

        if self._symbol_replace_value is None:
            return normalized_table_data

        return TableData(
            normalized_table_data.table_name,
            [
                replace_symbol(
                    replace_unprintable_char(header),
                    self._symbol_replace_value,
                    is_replace_consecutive_chars=True,
                    is_strip=True,
                )
                for header in normalized_table_data.headers
            ],
            normalized_table_data.rows,
            dp_extractor=normalized_table_data.dp_extractor,
            type_hints=table_data.dp_extractor.column_type_hints,
        )

    def write_completion_message(self) -> None:
        logger = self._logger

        logger.debug(f"----- {PROGRAM_NAME:s} completed -----")

        log_list = [
            "source={}".format(
                tcolor(
                    str(
                        self._con.fetch_value(
                            select="COUNT(DISTINCT({}))".format("source_id"),
                            table_name=SourceInfo.get_table_name(),
                        )
                    ),
                    color="light_white",
                )
            )
        ]
        if self.get_success_count() > 0:
            log_list.append(
                tcolor("success=", color="green")
                + tcolor(str(self.get_success_count()), color="light_green"),
            )
        if self._result_counter.fail_count > 0:
            log_list.append(
                tcolor("fail=", color="red")
                + tcolor(str(self._result_counter.fail_count), color="light_red"),
            )
        if self._result_counter.skip_count > 0:
            log_list.append(
                tcolor("skip=", color="yellow")
                + tcolor(str(self._result_counter.skip_count), color="light_yellow"),
            )
        if self._result_counter.created_table_count > 0:
            log_list.append(
                tcolor("created-table=", color="white")
                + tcolor(str(self._result_counter.skip_count), color="light_white"),
            )

        logger.info("converted results: {}".format(", ".join(log_list)))
        database_path_msg = "database path: {:s}".format(
            tcolor(Path(self._con.database_path).relpath(), color="light_white"),
        )

        if self.get_success_count() > 0:
            output_format, verbosity_level = self.__get_dump_param()
            logger.info(database_path_msg)

            try:
                logger.debug(
                    "----- database schema -----\n{}".format(
                        indent(
                            self._con.schema_extractor.dumps(
                                output_format=output_format, verbosity_level=verbosity_level
                            ),
                            "    ",
                        )
                    )
                )
            except:  # noqa
                # avoid crashes caused by logging
                pass
        else:
            logger.debug(database_path_msg)

    def _convert_nb(self, nb, source_info):
        success_count = self._result_counter.success_count
        created_table_set = convert_nb(
            logger=self._logger,
            source_info=source_info,
            con=self._con,
            result_logger=self._result_logger,
            nb=nb,
        )

        if self._result_counter.success_count == success_count:
            self._logger.warning(TABLE_NOT_FOUND_MSG_FORMAT.format(source_info.base_name))
            return

        return created_table_set

    def _convert_complex_json(self, json_loader: AbstractTableReader, source_info) -> Set[str]:
        from ._dict_converter import DictConverter

        dict_converter = DictConverter(
            self._logger,
            self._table_creator,
            source_info=source_info,
            index_list=self._index_list,
            max_workers=self._max_workers,
        )

        try:
            dict_converter.to_sqlite_table(json_loader.load_dict(), [])
        except AttributeError:
            pass

        return dict_converter.converted_table_name_set

    def __get_dump_param(self) -> Tuple[str, int]:
        found_ptw = True
        try:
            import pytablewriter  # noqa: W0611
        except ImportError:
            found_ptw = False

        if found_ptw:
            return ("rst_simple_table", self._verbosity_level)

        if self._verbosity_level >= 1:
            return ("text", MAX_VERBOSITY_LEVEL)

        if self._verbosity_level == 0:
            return ("text", 1)

        raise ValueError(f"invalid verbosity_level: {self._verbosity_level}")
