# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import msgfy
import path
import pytablereader as ptr
import six
from simplesqlite import SQLiteTableDataSanitizer

from .._common import dup_col_handler
from .._const import IPYNB_FORMAT_NAME_LIST, TABLE_NOT_FOUND_MSG_FORMAT
from .._ipynb_converter import is_ipynb_file_path, load_ipynb_file
from ._base import TableConverter


def _get_format_type_from_path(file_path):
    return file_path.ext.lstrip(".")


class FileConverter(TableConverter):
    def convert(self, file_path):
        file_path = path.Path(file_path)
        logger = self._logger
        con = self._con
        result_counter = self._result_counter

        if not file_path.isfile():
            logger.error("file not found: {}".format(file_path))
            result_counter.inc_fail()
            return

        if file_path.realpath() == con.database_path:
            logger.warn(
                "skip a file which has the same path as the output file ({})".format(file_path)
            )
            return

        logger.debug("converting '{}'".format(file_path))
        existing_table_count = result_counter.total_count
        dirname, basename, filesize, mtime = self.__get_source_info_base(file_path.realpath())
        source_info_record_base = {
            "dir_name": dirname,
            "base_name": basename,
            "size": filesize,
            "mtime": mtime,
        }

        if self._format_name in IPYNB_FORMAT_NAME_LIST or is_ipynb_file_path(file_path):
            import nbformat

            try:
                created_table_name_set = self._convert_nb(
                    nb=load_ipynb_file(file_path, encoding=self._encoding), source=file_path
                )
            except nbformat.reader.NotJSONError as e:
                logger.error(e)
                return

            for table_name in created_table_name_set:
                record = source_info_record_base.copy()
                record.update({
                    "format_name": "ipynb",
                    "dst_table_name": table_name,
                })
                self._add_source_info(**record)

            return

        try:
            loader = ptr.TableFileLoader(
                file_path, format_name=self._format_name, encoding=self._encoding
            )
        except ptr.InvalidFilePathError as e:
            logger.debug(msgfy.to_debug_message(e))
            result_counter.inc_fail()
            return
        except ptr.LoaderNotFoundError:
            logger.debug("loader not found that coincide with '{}'".format(file_path))
            result_counter.inc_fail()
            return

        source_info_record_base["format_name"] = loader.format_name

        try:
            for table_data in loader.load():
                logger.debug("loaded tabledata: {}".format(six.text_type(table_data)))

                sqlite_tabledata = SQLiteTableDataSanitizer(
                    table_data, dup_col_handler=dup_col_handler
                ).normalize()

                try:
                    self._table_creator.create(sqlite_tabledata, self._index_list, source=file_path)
                except (ValueError, IOError) as e:
                    logger.debug(
                        "exception={:s}, path={}, message={}".format(type(e).__name__, file_path, e)
                    )
                    result_counter.inc_fail()
                    return

                record = source_info_record_base.copy()
                record.update({"dst_table_name": sqlite_tabledata.table_name})
                self._add_source_info(**record)
        except ptr.OpenError as e:
            logger.error(
                "{:s}: open error: file={}, message='{}'".format(
                    e.__class__.__name__, file_path, str(e)
                )
            )
            result_counter.inc_fail()
        except ptr.ValidationError as e:
            if loader.format_name == "json":
                for table_name in self._convert_complex_json(loader.loader):
                    record = source_info_record_base.copy()
                    record.update({"dst_table_name": table_name})
                    self._add_source_info(**record)
            else:
                logger.error(
                    "{:s}: invalid {} data format: path={}, message={}".format(
                        e.__class__.__name__,
                        _get_format_type_from_path(file_path),
                        file_path,
                        str(e),
                    )
                )
                result_counter.inc_fail()
        except ptr.DataError as e:
            logger.error(
                "{:s}: invalid {} data: path={}, message={}".format(
                    e.__class__.__name__, _get_format_type_from_path(file_path), file_path, str(e)
                )
            )
            result_counter.inc_fail()

        if result_counter.total_count == existing_table_count:
            logger.warn(TABLE_NOT_FOUND_MSG_FORMAT.format(file_path))

    @staticmethod
    def __get_source_info_base(source):
        return (source.dirname(), source.basename(), source.getsize(), source.getmtime())
