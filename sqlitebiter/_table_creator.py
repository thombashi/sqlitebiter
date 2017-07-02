#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

import simplesqlite
from sqliteschema import SqliteSchemaExtractor


class TableCreator(object):

    def __init__(self, logger, dst_con):
        self.__logger = logger
        self.__dst_con = dst_con

    def create(self, tabledata):
        is_rename, con_mem = self.__require_rename_table(tabledata)
        src_table_name = con_mem.get_table_name_list()[0]
        dst_table_name = src_table_name

        if is_rename:
            dst_table_name = self.__make_unique_table_name(src_table_name)

            self.__logger.debug(u"rename table from '{}' to '{}'".format(
                src_table_name, dst_table_name))

            simplesqlite.copy_table(
                src_con=con_mem, dst_con=self.__dst_con,
                src_table_name=src_table_name,
                dst_table_name=dst_table_name)
        else:
            simplesqlite.append_table(
                src_con=con_mem, dst_con=self.__dst_con,
                table_name=dst_table_name)

    def __require_rename_table(self, tabledata):
        con_mem = simplesqlite.connect_sqlite_db_mem()
        con_mem.create_table_from_tabledata(tabledata=tabledata)

        if not self.__dst_con.has_table(tabledata.table_name):
            return (False, con_mem)

        if self.__dst_con.get_attr_name_list(tabledata.table_name) != tabledata.header_list:
            return (True, con_mem)

        con_schema_extractor = SqliteSchemaExtractor(
            self.__dst_con, verbosity_level=1)
        con_mem_schema_extractor = SqliteSchemaExtractor(
            con_mem, verbosity_level=1)

        if con_schema_extractor.get_database_schema() == con_mem_schema_extractor.get_database_schema():
            return (False, con_mem)

        return (True, con_mem)

    def __make_unique_table_name(self, table_name_base):
        exist_table_name_list = self.__dst_con.get_table_name_list()

        if table_name_base not in exist_table_name_list:
            return table_name_base

        suffix_id = 1
        while True:
            table_name_candidate = u"{:s}_{:d}".format(
                table_name_base, suffix_id)

            if table_name_candidate not in exist_table_name_list:
                return table_name_candidate

            suffix_id += 1
