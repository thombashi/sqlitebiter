"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import errno
import os
import re
import sys
from copy import deepcopy
from typing import Dict, Optional, Pattern, Type
from urllib.parse import urlparse

import msgfy
import pytablereader as ptr
import simplesqlite as sqlite
from pytablereader.interface import AbstractTableReader
from typepy.type import AbstractType

from .._const import IPYNB_FORMAT_NAME_LIST, TABLE_NOT_FOUND_MSG_FORMAT, ExitCode
from ._base import SourceInfo, TableConverter
from ._common import TYPE_HINT_FROM_HEADER_RULES, normalize_type_hint
from ._ipynb_converter import is_ipynb_url, load_ipynb_url


TypeHintRules = Dict[Pattern, Type[AbstractType]]


def parse_source_info_url(url: str) -> SourceInfo:
    result = urlparse(url)

    source_info = SourceInfo()
    source_info.dir_name = result.netloc + os.path.dirname(result.path)  # type: ignore
    source_info.base_name = os.path.basename(str(result.path))

    return source_info


def create_url_loader(
    logger,
    source_url: str,
    format_name: str,
    encoding: str,
    type_hint_rules: Optional[TypeHintRules],
    proxies: Optional[Dict],
) -> AbstractTableReader:
    try:
        return ptr.TableUrlLoader(
            source_url,
            format_name,
            encoding=encoding,
            type_hint_rules=type_hint_rules,
            proxies=proxies,
        )
    except (ptr.HTTPError, ptr.UrlError) as e:
        logger.error(msgfy.to_error_message(e))
        sys.exit(ExitCode.FAILED_HTTP)
    except ptr.ProxyError as e:
        logger.error(msgfy.to_error_message(e))
        sys.exit(errno.ECONNABORTED)


class UrlConverter(TableConverter):
    def __init__(
        self,
        logger,
        con,
        symbol_replace_value,
        add_pri_key_name,
        convert_configs,
        index_list,
        is_type_inference,
        is_type_hint_header,
        verbosity_level,
        format_name,
        encoding,
        proxy,
    ):
        super().__init__(
            logger,
            con,
            symbol_replace_value=symbol_replace_value,
            add_pri_key_name=add_pri_key_name,
            convert_configs=convert_configs,
            index_list=index_list,
            is_type_inference=is_type_inference,
            is_type_hint_header=is_type_hint_header,
            verbosity_level=verbosity_level,
            format_name=format_name,
            encoding=encoding,
        )

        self.__proxy = proxy

    def convert(self, url: str) -> None:
        logger = self._logger
        result_counter = self._result_counter

        source_info_record_base = parse_source_info_url(url)
        source_info_record_base.source_id = self._fetch_next_source_id()

        if self._format_name in IPYNB_FORMAT_NAME_LIST or is_ipynb_url(url):
            try:
                nb, nb_size = load_ipynb_url(url, proxies=self.__get_proxies())
            except RuntimeError as e:
                logger.error(e)
                return

            changed_table_name_set = self._convert_nb(nb, source_info=source_info_record_base)

            for table_name in changed_table_name_set:
                record = deepcopy(source_info_record_base)
                record.format_name = "ipynb"
                record.dst_table = table_name
                record.size = nb_size
                SourceInfo.insert(record)

            return

        loader = self.__create_loader(url)
        source_info_record_base.format_name = loader.format_name
        success_count = result_counter.success_count

        try:
            for table_data in loader.load():
                logger.debug("loaded table_data: {}".format(str(table_data)))

                sqlite_tabledata = self.normalize_table(table_data)

                try:
                    self._table_creator.create(
                        sqlite_tabledata, self._index_list, source_info=source_info_record_base
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

                record = deepcopy(source_info_record_base)
                record.dst_table = sqlite_tabledata.table_name
                SourceInfo.insert(record)
        except ptr.ValidationError as e:
            if loader.format_name == "json":
                for table_name in self._convert_complex_json(
                    loader.loader, source_info_record_base
                ):
                    record = deepcopy(source_info_record_base)
                    record.dst_table = table_name
                    SourceInfo.insert(record)
            else:
                logger.error("{:s}: url={}, message={}".format(e.__class__.__name__, url, str(e)))
                result_counter.inc_fail()
        except ptr.DataError as e:
            logger.error(
                "{:s}: invalid data: url={}, message={}".format(e.__class__.__name__, url, str(e))
            )
            result_counter.inc_fail()
        except OverflowError as e:
            logger.error("{}: {}".format(url, e))
            result_counter.inc_fail()

        if result_counter.success_count == success_count:
            logger.warning(TABLE_NOT_FOUND_MSG_FORMAT.format(url))

    def __get_proxies(self) -> Dict:
        return {"http": self.__proxy, "https": self.__proxy}

    def __create_loader(self, url: str) -> AbstractTableReader:
        logger = self._logger
        type_hint_rules = self.__extract_type_hint_rules(url)
        proxies = self.__get_proxies()

        try:
            return create_url_loader(
                logger, url, self._format_name, self._encoding, type_hint_rules, proxies
            )
        except ptr.LoaderNotFoundError as e:
            logger.debug(e)

        try:
            return create_url_loader(logger, url, "html", self._encoding, type_hint_rules, proxies)
        except ptr.LoaderNotFoundError as e:
            logger.error(msgfy.to_error_message(e))
            sys.exit(ExitCode.FAILED_LOADER_NOT_FOUND)

    def __extract_type_hint_rules(self, url: str) -> TypeHintRules:
        if self._is_type_hint_header:
            return TYPE_HINT_FROM_HEADER_RULES

        type_hint_rules = {}

        for config in self._convert_configs:
            if not isinstance(config, dict):
                self._logger.debug("unexpected config value: {}".format(config))
                continue

            if config.get("target_url") not in url:  # type: ignore
                continue

            for pattern, params in config["rules"].items():
                if not params.get("type hint"):
                    continue

                type_hint_rules[re.compile(pattern, re.IGNORECASE)] = normalize_type_hint(
                    params["type hint"]
                )

        return type_hint_rules
