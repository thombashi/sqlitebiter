# encoding: utf-8

'''
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
'''

from __future__ import absolute_import, unicode_literals

from sqliteschema import SQLiteSchemaExtractor

from .._const import MAX_VERBOSITY_LEVEL, PROGRAM_NAME
from .._counter import ResultCounter
from .._table_creator import TableCreator


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
        self._table_creator = TableCreator(logger=self._logger, dst_con=con)

    def get_return_code(self):
        return self._result_counter.get_return_code()

    def get_success_count(self):
        return self._result_counter.success_count

    def write_completion_message(self):
        logger = self._logger
        database_path_msg = "database path: {:s}".format(self._con.database_path)

        logger.debug("----- {:s} completed -----".format(PROGRAM_NAME))
        logger.info("number of created tables: {:d}".format(self.get_success_count()))
        if self.get_success_count() > 0:
            output_format, verbosity_level = self.__get_dump_param()
            logger.info(database_path_msg)

            try:
                from textwrap import indent
            except ImportError:
                # for Python 2 compatibility
                def indent(value, _):
                    return value

            logger.debug("----- database schema -----\n{}".format(
                indent(self._schema_extractor.dumps(
                    output_format=output_format, verbosity_level=verbosity_level), "    ")))
        else:
            logger.debug(database_path_msg)

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
