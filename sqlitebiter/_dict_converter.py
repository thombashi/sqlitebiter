# encoding: utf-8

'''
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
'''

from __future__ import absolute_import

import re

import msgfy
import pytablereader as ptr
import six

from ._common import get_success_message


class DictConverter(object):

    def __init__(
            self, logger, table_creator, result_counter, schema_extractor, verbosity_level,
            source, index_list):
        self.__logger = logger
        self.__table_creator = table_creator
        self.__result_counter = result_counter
        self.__index_list = index_list
        self.__verbosity_level = verbosity_level
        self.__source = source
        self.__schema_extractor = schema_extractor

    def to_sqlite_table(self, data, key_list):
        if not data:
            return

        root_maps = {}

        for key, v in data.items():
            if isinstance(v, (six.text_type, int, float)) or v is None:
                root_maps[key] = v
                continue

            loader = ptr.JsonTableDictLoader(v)

            try:
                for table_data in loader.load():
                    if re.search("json[0-9]+", table_data.table_name):
                        table_data.table_name = self.__make_table_name(key_list + [key])
                    else:
                        table_data.table_name = self.__make_table_name(
                            key_list + [key, table_data.table_name])

                    self.__write(table_data)
            except ptr.DataError:
                self.to_sqlite_table(v, key_list + [key])
            except ptr.ValidationError as e:
                self.__logger.debug(msgfy.to_debug_message(e))

        if not root_maps:
            return

        loader = ptr.JsonTableDictLoader(root_maps)
        for table_data in loader.load():
            if key_list:
                table_data.table_name = self.__make_table_name(key_list)
            else:
                table_data.table_name = "root"

            self.__write(table_data)

    def __make_table_name(self, key_list):
        return "_".join(key_list)

    def __write(self, table_data):
        from simplesqlite import SQLiteTableDataSanitizer

        self.__logger.debug(u"loaded tabledata: {}".format(six.text_type(table_data)))

        sqlite_tabledata = SQLiteTableDataSanitizer(table_data).normalize()
        self.__table_creator.create(sqlite_tabledata, self.__index_list)
        self.__result_counter.inc_success()

        self.__logger.info(get_success_message(
            self.__source, self.__schema_extractor, sqlite_tabledata.table_name,
            self.__verbosity_level))
