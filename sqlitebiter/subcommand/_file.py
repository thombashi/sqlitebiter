# encoding: utf-8

'''
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
'''

from __future__ import absolute_import, unicode_literals

import msgfy
import path
import pytablereader as ptr
import six
from simplesqlite import SQLiteTableDataSanitizer

from .._common import dup_col_handler, get_success_message
from .._const import IPYNB_FORMAT_NAME_LIST, TABLE_NOT_FOUND_MSG_FORMAT
from .._ipynb_converter import convert_nb, is_ipynb_file_path, load_ipynb_file
from ._base import TableConverter


def _get_format_type_from_path(file_path):
    return file_path.ext.lstrip(".")


class FileConverter(TableConverter):

    def convert(self, file_path):
        file_path = path.Path(file_path)
        file_real_path = file_path.realpath()
        logger = self._logger
        con = self._con
        verbosity_level = self._verbosity_level
        result_counter = self._result_counter

        if not file_path.isfile():
            logger.error("file not found: {}".format(file_path))
            result_counter.inc_fail()
            return

        if file_real_path == con.database_path:
            logger.warn(
                "skip a file which has the same path as the output file ({})".format(file_path))
            return

        logger.debug("converting '{}'".format(file_path))
        existing_table_count = result_counter.total_count

        if self._format_name in IPYNB_FORMAT_NAME_LIST or is_ipynb_file_path(file_path):
            convert_nb(
                logger,
                con,
                result_counter,
                nb=load_ipynb_file(file_path, encoding=self._encoding),
                source_id=self._fetch_next_source_id())
            for table_name in con.fetch_table_name_list():
                logger.info(get_success_message(
                    file_path, self._schema_extractor, table_name, verbosity_level))
                result_counter.inc_success()
            if result_counter.total_count == existing_table_count:
                logger.warn(TABLE_NOT_FOUND_MSG_FORMAT.format(file_path))

            self._add_source_info(
                file_real_path.dirname(), file_real_path.basename(), format_name="ipynb",
                size=file_path.getsize(), mtime=file_path.getmtime())
            return

        try:
            loader = ptr.TableFileLoader(
                file_path, format_name=self._format_name, encoding=self._encoding)
        except ptr.InvalidFilePathError as e:
            logger.debug(msgfy.to_debug_message(e))
            result_counter.inc_fail()
            return
        except ptr.LoaderNotFoundError:
            logger.debug("loader not found that coincide with '{}'".format(file_path))
            result_counter.inc_fail()
            return

        source_info_record = (
            file_real_path.dirname(), file_real_path.basename(), loader.format_name,
            file_path.getsize(), file_path.getmtime())

        try:
            for table_data in loader.load():
                logger.debug("loaded tabledata: {}".format(six.text_type(table_data)))

                sqlite_tabledata = SQLiteTableDataSanitizer(
                    table_data, dup_col_handler=dup_col_handler).normalize()

                try:
                    self._table_creator.create(sqlite_tabledata, self._index_list)
                    result_counter.inc_success()
                except (ValueError, IOError) as e:
                    logger.debug("exception={:s}, path={}, message={}".format(
                        type(e).__name__, file_path, e))
                    result_counter.inc_fail()
                    return

                logger.info(get_success_message(
                    file_path, self._schema_extractor, sqlite_tabledata.table_name,
                    verbosity_level))

            self._add_source_info(*source_info_record)
        except ptr.OpenError as e:
            logger.error("{:s}: open error: file={}, message='{}'".format(
                e.__class__.__name__, file_path, str(e)))
            result_counter.inc_fail()
        except ptr.ValidationError as e:
            if loader.format_name == "json" and self._convert_complex_json(loader.loader):
                result_counter.inc_success()
                self._add_source_info(*source_info_record)
            else:
                logger.error("{:s}: invalid {} data format: path={}, message={}".format(
                    e.__class__.__name__, _get_format_type_from_path(file_path), file_path, str(e)))
                result_counter.inc_fail()
        except ptr.DataError as e:
            logger.error("{:s}: invalid {} data: path={}, message={}".format(
                e.__class__.__name__, _get_format_type_from_path(file_path), file_path, str(e)))
            result_counter.inc_fail()

        if result_counter.total_count == existing_table_count:
            logger.warn(TABLE_NOT_FOUND_MSG_FORMAT.format(file_path))
