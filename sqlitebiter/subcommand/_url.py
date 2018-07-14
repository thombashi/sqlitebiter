# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import errno
import os
import sys

import msgfy
import pytablereader as ptr
import simplesqlite as sqlite
import six
from six.moves.urllib.parse import urlparse

from .._common import dup_col_handler
from .._const import IPYNB_FORMAT_NAME_LIST, TABLE_NOT_FOUND_MSG_FORMAT
from .._enum import ExitCode
from .._ipynb_converter import is_ipynb_url, load_ipynb_url
from ._base import TableConverter


def get_logging_url_path(url):
    result = urlparse(url)

    return result.netloc + result.path


def parse_source_info_url(url):
    result = urlparse(url)

    return (result.netloc + os.path.dirname(result.path), os.path.basename(result.path))


def create_url_loader(logger, source_url, format_name, encoding, proxies):
    try:
        return ptr.TableUrlLoader(source_url, format_name, encoding=encoding, proxies=proxies)
    except ptr.HTTPError as e:
        logger.error(msgfy.to_error_message(e))
        sys.exit(ExitCode.FAILED_HTTP)
    except ptr.ProxyError as e:
        logger.error(msgfy.to_error_message(e))
        sys.exit(errno.ECONNABORTED)


class UrlConverter(TableConverter):
    def __init__(self, logger, con, index_list, verbosity_level, format_name, encoding, proxy):
        super(UrlConverter, self).__init__(
            logger, con, index_list, verbosity_level, format_name, encoding
        )

        self.__proxy = proxy

    def convert(self, url):
        logger = self._logger
        result_counter = self._result_counter
        url_dir_name, url_base_name = parse_source_info_url(url)
        source_info_record_base = {
            "dir_name": url_dir_name,
            "base_name": url_base_name,
        }

        if self._format_name in IPYNB_FORMAT_NAME_LIST or is_ipynb_url(url):
            nb, nb_size = load_ipynb_url(url, proxies=self.__get_proxies())
            created_table_name_set = self._convert_nb(nb, source=get_logging_url_path(url))

            for table_name in created_table_name_set:
                record = source_info_record_base.copy()
                record.update({
                    "format_name": "ipynb",
                    "dst_table_name": table_name,
                    "size": nb_size
                })
                self._add_source_info(**record)

            return

        loader = self.__create_loader(url)
        source_info_record_base["format_name"] = loader.format_name

        try:
            for table_data in loader.load():
                logger.debug("loaded table_data: {}".format(six.text_type(table_data)))

                sqlite_tabledata = sqlite.SQLiteTableDataSanitizer(
                    table_data, dup_col_handler=dup_col_handler
                ).normalize()

                try:
                    self._table_creator.create(
                        sqlite_tabledata, self._index_list, source=get_logging_url_path(url)
                    )
                except sqlite.OperationalError as e:
                    logger.error(
                        "{:s}: failed to convert: url={}, message={}".format(
                            e.__class__.__name__, url, e.message
                        )
                    )
                    result_counter.inc_fail()
                    continue
                except ValueError as e:
                    logger.debug(
                        "{:s}: url={}, message={}".format(e.__class__.__name__, url, str(e))
                    )
                    result_counter.inc_fail()
                    continue

                record = source_info_record_base.copy()
                record.update({"dst_table_name": sqlite_tabledata.table_name})
                self._add_source_info(**record)
        except ptr.ValidationError as e:
            if loader.format_name == "json":
                for table_name in self._convert_complex_json(loader.loader):
                    record = source_info_record_base.copy()
                    record.update({"dst_table_name": table_name})
                    self._add_source_info(**record)
            else:
                logger.error("{:s}: url={}, message={}".format(e.__class__.__name__, url, str(e)))
                result_counter.inc_fail()
        except ptr.DataError as e:
            logger.error(
                "{:s}: invalid data: url={}, message={}".format(e.__class__.__name__, url, str(e))
            )
            result_counter.inc_fail()

        if result_counter.total_count == 0:
            logger.warn(TABLE_NOT_FOUND_MSG_FORMAT.format(url))

    def __get_proxies(self):
        return {"http": self.__proxy, "https": self.__proxy}

    def __create_loader(self, url):
        logger = self._logger
        proxies = self.__get_proxies()

        try:
            return create_url_loader(logger, url, self._format_name, self._encoding, proxies)
        except ptr.LoaderNotFoundError as e:
            logger.debug(e)

        try:
            return create_url_loader(logger, url, "html", self._encoding, proxies)
        except ptr.LoaderNotFoundError as e:
            logger.error(msgfy.to_error_message(e))
            sys.exit(ExitCode.FAILED_LOADER_NOT_FOUND)
