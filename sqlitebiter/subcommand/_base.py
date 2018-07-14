# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

from simplesqlite.query import And, Attr, Where
from sqliteschema import SQLiteSchemaExtractor

from .._common import ResultLogger
from .._const import (
    MAX_VERBOSITY_LEVEL,
    PROGRAM_NAME,
    SOURCE_INFO_TABLE,
    TABLE_NOT_FOUND_MSG_FORMAT,
)
from .._counter import ResultCounter
from .._ipynb_converter import convert_nb
from .._table_creator import TableCreator


class SourceInfo(object):
    SOURCE_ID = "source_id"
    DIR_NAME = "dir_name"
    BASE_NAME = "base_name"
    FORMAT_NAME = "format"
    SIZE = "size"
    MTIME = "mtime"


class TableConverter(object):
    def __init__(self, logger, con, index_list, verbosity_level, format_name=None, encoding=None):
        self._logger = logger
        self._con = con
        self._index_list = index_list
        self._verbosity_level = verbosity_level
        self._format_name = format_name
        self._encoding = encoding

        self._schema_extractor = SQLiteSchemaExtractor(con)
        self._result_counter = ResultCounter()
        self._result_logger = ResultLogger(
            logger, self._schema_extractor, self._result_counter, self._verbosity_level
        )
        self._table_creator = TableCreator(
            logger=self._logger,
            dst_con=con,
            result_logger=self._result_logger,
            verbosity_level=verbosity_level,
        )

        self._con.create_table(
            SOURCE_INFO_TABLE,
            [
                "{:s} INTEGER PRIMARY KEY AUTOINCREMENT".format(SourceInfo.SOURCE_ID),
                "{:s} TEXT".format(SourceInfo.DIR_NAME),
                "{:s} TEXT NOT NULL".format(SourceInfo.BASE_NAME),
                "{:s} TEXT NOT NULL".format(SourceInfo.FORMAT_NAME),
                "{:s} INTEGER".format(SourceInfo.SIZE),
                "{:s} INTEGER".format(SourceInfo.MTIME),
            ],
        )

    def _fetch_source_id(self, dir_name, base_name, format_name, size=None, mtime=None):
        where_list = []
        if dir_name:
            where_list.append(Where(SourceInfo.DIR_NAME, dir_name))
        where_list.extend(
            [Where(SourceInfo.BASE_NAME, base_name), Where(SourceInfo.FORMAT_NAME, format_name)]
        )
        if size:
            where_list.append(Where(SourceInfo.SIZE, size))
        if mtime:
            where_list.append(Where(SourceInfo.MTIME, mtime))

        return self._con.fetch_value(
            select=Attr(SourceInfo.SOURCE_ID), table_name=SOURCE_INFO_TABLE, where=And(where_list)
        )

    def _fetch_next_source_id(self):
        source_id = self._con.fetch_value(
            select="MAX({})".format(Attr(SourceInfo.SOURCE_ID)), table_name=SOURCE_INFO_TABLE
        )

        if source_id is None:
            return 1

        return source_id + 1

    def _add_source_info(self, dir_name, base_name, format_name, size=None, mtime=None):
        self._con.insert(SOURCE_INFO_TABLE, (None, dir_name, base_name, format_name, size, mtime))

    def get_return_code(self):
        return self._result_counter.get_return_code()

    def get_success_count(self):
        return self._result_counter.success_count

    def write_completion_message(self):
        logger = self._logger
        database_path_msg = "database path: {:s}".format(self._con.database_path)

        logger.debug("----- {:s} completed -----".format(PROGRAM_NAME))
        logger.info(
            "converted results: sources={}, success={} tables={}".format(
                1, self.get_success_count(), self._result_counter.created_table_count
            )
        )
        if self.get_success_count() > 0:
            output_format, verbosity_level = self.__get_dump_param()
            logger.info(database_path_msg)

            try:
                from textwrap import indent
            except ImportError:
                # for Python 2 compatibility
                def indent(value, _):
                    return value

            logger.debug(
                "----- database schema -----\n{}".format(
                    indent(
                        self._schema_extractor.dumps(
                            output_format=output_format, verbosity_level=verbosity_level
                        ),
                        "    ",
                    )
                )
            )
        else:
            logger.debug(database_path_msg)

    def _convert_nb(self, nb, source):
        created_table_set = convert_nb(
            self._logger,
            source,
            self._con,
            self._result_logger,
            nb=nb,
            source_id=self._fetch_next_source_id(),
        )

        if not created_table_set:
            self._logger.warn(TABLE_NOT_FOUND_MSG_FORMAT.format(source))

        return created_table_set

    def _convert_complex_json(self, json_loader):
        from .._dict_converter import DictConverter

        dict_converter = DictConverter(
            self._logger,
            self._table_creator,
            source=json_loader.source,
            index_list=self._index_list,
        )
        is_success = False

        try:
            dict_converter.to_sqlite_table(json_loader.load_dict(), [])
        except AttributeError:
            pass
        else:
            is_success = True

        return is_success

    def __get_dump_param(self):
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

        raise ValueError("invalid verbosity_level: {}".format(self._verbosity_level))
