# encoding: utf-8

'''
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
'''

from __future__ import absolute_import, unicode_literals

import errno
import sys

import msgfy
import pytablereader as ptr
import simplesqlite as sqlite
import six

from .._common import dup_col_handler, get_success_message
from .._const import IPYNB_FORMAT_NAME_LIST, TABLE_NOT_FOUND_MSG_FORMAT
from .._dict_converter import DictConverter
from .._enum import ExitCode
from .._ipynb_converter import convert_nb, is_ipynb_url, load_ipynb_url
from ._base import TableConverter


def get_logging_url_path(url):
    from six.moves.urllib.parse import urlparse

    result = urlparse(url)

    return result.netloc + result.path


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
            logger, con, index_list, verbosity_level, format_name, encoding)

        self.__proxy = proxy

    def convert(self, url):
        logger = self._logger
        con = self._con
        verbosity_level = self._verbosity_level
        result_counter = self._result_counter

        if self._format_name in IPYNB_FORMAT_NAME_LIST or is_ipynb_url(url):
            convert_nb(
                logger, con, result_counter, nb=load_ipynb_url(url, proxies=self.__get_proxies()))
            for table_name in con.fetch_table_name_list():
                logger.info(get_success_message(
                    get_logging_url_path(url), self._schema_extractor, table_name,
                    verbosity_level))
                result_counter.inc_success()
            if result_counter.total_count == 0:
                TABLE_NOT_FOUND_MSG_FORMAT.format(url)
            else:
                self.write_completion_message()

            sys.exit(self.get_return_code())

        loader = self.__create_loader(url)

        try:
            for table_data in loader.load():
                logger.debug("loaded table_data: {}".format(six.text_type(table_data)))

                sqlite_tabledata = sqlite.SQLiteTableDataSanitizer(
                    table_data, dup_col_handler=dup_col_handler).normalize()

                try:
                    self._table_creator.create(sqlite_tabledata, self._index_list)
                    result_counter.inc_success()
                except sqlite.OperationalError as e:
                    logger.error("{:s}: failed to convert: url={}, message={}".format(
                        e.__class__.__name__, url, e.message))
                    result_counter.inc_fail()
                    continue
                except ValueError as e:
                    logger.debug("{:s}: url={}, message={}".format(
                        e.__class__.__name__, url, str(e)))
                    result_counter.inc_fail()
                    continue

                logger.info(get_success_message(
                    get_logging_url_path(url), self._schema_extractor, sqlite_tabledata.table_name,
                    verbosity_level))
        except ptr.ValidationError as e:
            is_fail = True
            if loader.format_name == "json":
                dict_converter = DictConverter(
                    logger, self._table_creator, result_counter, self._schema_extractor,
                    verbosity_level, source=url, index_list=self._index_list)

                try:
                    dict_converter.to_sqlite_table(loader.loader.load_dict(), [])
                except AttributeError:
                    pass
                else:
                    is_fail = False

            if is_fail:
                logger.error("{:s}: url={}, message={}".format(e.__class__.__name__, url, str(e)))
                result_counter.inc_fail()
        except ptr.DataError as e:
            logger.error("{:s}: invalid data: url={}, message={}".format(
                e.__class__.__name__, url, str(e)))
            result_counter.inc_fail()

        if result_counter.total_count == 0:
            logger.warn(TABLE_NOT_FOUND_MSG_FORMAT.format(url))

    def __get_proxies(self):
        return {
            "http": self.__proxy,
            "https": self.__proxy,
        }

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
