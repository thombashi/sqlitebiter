"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import sys
from copy import deepcopy
from typing import Dict, Optional, Pattern, Type

import msgfy
import pytablereader as ptr
import simplesqlite as sqlite
from pytablereader.interface import AbstractTableReader
from typepy.type import AbstractType

from .._const import IPYNB_FORMAT_NAME_LIST, TABLE_NOT_FOUND_MSG_FORMAT, ExitCode
from ._base import SourceInfo, TableConverter
from ._common import TYPE_HINT_FROM_HEADER_RULES
from ._ipynb_converter import load_ipynb_text


TypeHintRules = Dict[Pattern, Type[AbstractType]]


def create_text_loader(
    logger,
    text: str,
    format_name: str,
    encoding: str,
    type_hint_rules: Optional[TypeHintRules],
) -> AbstractTableReader:
    try:
        return ptr.TableTextLoader(
            text,
            format_name,
            encoding=encoding,
            type_hint_rules=type_hint_rules,
        )
    except (ptr.LoaderNotFoundError) as e:
        logger.error(msgfy.to_error_message(e))
        sys.exit(ExitCode.FAILED_LOADER_NOT_FOUND)


class TextConverter(TableConverter):
    def __get_source_info_base(self, text: str) -> SourceInfo:
        return SourceInfo(
            base_name="stdin",
            size=len(text),
            source_id=self._fetch_next_source_id(),
        )

    def convert(self, text: str) -> None:
        logger = self._logger
        result_counter = self._result_counter
        source_info_record_base = self.__get_source_info_base(text)

        if self._format_name in IPYNB_FORMAT_NAME_LIST:
            try:
                nb, nb_size = load_ipynb_text(text)
            except RuntimeError as e:
                logger.error(e)
                return

            changed_table_name_set = self._convert_nb(nb, source_info=source_info_record_base)

            for table_name in changed_table_name_set:
                record = deepcopy(source_info_record_base)
                record.format_name = "ipynb"  # type: ignore
                record.dst_table = table_name
                record.size = nb_size
                SourceInfo.insert(record)

            return

        loader = create_text_loader(
            logger,
            text,
            self._format_name,
            self._encoding,
            TYPE_HINT_FROM_HEADER_RULES if self._is_type_hint_header else None,
        )
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
                        "{:s}: failed to convert: text={}, message={}".format(
                            e.__class__.__name__, text, e.message
                        )
                    )
                    result_counter.inc_fail()
                    continue
                except ValueError as e:
                    logger.debug(
                        "{:s}: text={}, message={}".format(e.__class__.__name__, text, str(e))
                    )
                    result_counter.inc_fail()
                    continue

                record = deepcopy(source_info_record_base)
                record.dst_table = sqlite_tabledata.table_name  # type: ignore
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
                logger.error("{:s}: text={}, message={}".format(e.__class__.__name__, text, str(e)))
                result_counter.inc_fail()
        except ptr.DataError as e:
            logger.error(
                "{:s}: invalid data: text={}, message={}".format(e.__class__.__name__, text, str(e))
            )
            result_counter.inc_fail()
        except OverflowError as e:
            logger.error("{}: {}".format(text, e))
            result_counter.inc_fail()

        if result_counter.success_count == success_count:
            logger.warning(TABLE_NOT_FOUND_MSG_FORMAT.format(text))
