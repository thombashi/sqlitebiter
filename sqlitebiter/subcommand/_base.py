# encoding: utf-8

'''
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
'''

from __future__ import absolute_import, unicode_literals

from .._common import get_schema_extractor
from .._const import MAX_VERBOSITY_LEVEL, PROGRAM_NAME
from .._counter import ResultCounter
from .._table_creator import TableCreator


class TableConverter(object):

    @property
    def result_counter(self):
        return self._result_counter

    def __init__(self, logger, con, index_list, verbosity_level, format_name=None, encoding=None):
        self._logger = logger
        self._con = con
        self._index_list = index_list
        self._verbosity_level = verbosity_level
        self._format_name = format_name
        self._encoding = encoding

        self._schema_extractor = get_schema_extractor(con, verbosity_level)
        self._result_counter = ResultCounter()
        self._table_creator = TableCreator(logger=self._logger, dst_con=con)

    def get_return_code(self):
        return self._result_counter.get_return_code()

    def write_completion_message(self):
        logger = self._logger
        database_path_msg = "database path: {:s}".format(self._con.database_path)

        logger.debug("----- {:s} completed -----".format(PROGRAM_NAME))
        logger.info("number of created tables: {:d}".format(self._result_counter.success_count))
        if self._result_counter.success_count > 0:
            logger.info(database_path_msg)
            logger.debug("----- database schema -----")
            logger.debug(get_schema_extractor(
                self._con.database_path, MAX_VERBOSITY_LEVEL).dumps())
        else:
            logger.debug(database_path_msg)
