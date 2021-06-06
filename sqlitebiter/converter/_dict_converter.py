"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import re
from collections import OrderedDict
from typing import List, Sequence, Set, cast

import msgfy
import pytablereader as ptr
from simplesqlite import SQLiteTableDataSanitizer
from tabledata import TableData

from ._base import SourceInfo
from ._table_creator import TableCreator


class DictConverter:
    @property
    def converted_table_name_set(self) -> Set[str]:
        return self.__converted_table_name_set

    def __init__(
        self,
        logger,
        table_creator: TableCreator,
        source_info: SourceInfo,
        index_list: Sequence[str],
        max_workers: int,
    ) -> None:
        self.__logger = logger
        self.__table_creator = table_creator
        self.__index_list = index_list
        self.__source_info = source_info
        self.__max_workers = max_workers
        self.__converted_table_name_set: Set[str] = set()

    def to_sqlite_table(self, data: OrderedDict, keys: List[str]) -> None:
        if not data:
            return

        self.__logger.debug(f"to_sqlite_table: {type(data)}, keys={keys}")

        if isinstance(data, (list, tuple)):  # type: ignore
            for s in data:
                self.to_sqlite_table(s, keys)
            return

        root_maps = {}

        for key, v in data.items():
            if isinstance(v, (str, float) + (int,)) or v is None:
                root_maps[key] = v
                continue

            loader = ptr.JsonTableDictLoader(v)

            try:
                for table_data in loader.load():
                    if re.search("json[0-9]+", table_data.table_name):
                        table_data.table_name = self.__make_table_name(keys + [key])
                    else:
                        table_data.table_name = self.__make_table_name(
                            keys + [key, table_data.table_name]
                        )

                    self.__convert(table_data)
            except ptr.DataError:
                self.to_sqlite_table(v, keys + [key])
            except ptr.ValidationError as e:
                self.__logger.debug(msgfy.to_debug_message(e))

        if not root_maps:
            return

        loader = ptr.JsonTableDictLoader(root_maps)
        for table_data in loader.load():
            if keys:
                table_data.table_name = self.__make_table_name(keys)
            else:
                table_data.table_name = "root"

            self.__convert(table_data)

    def __make_table_name(self, keys: Sequence[str]) -> str:
        return "_".join(keys)

    def __convert(self, table_data: TableData) -> None:
        self.__logger.debug(f"loaded tabledata: {str(table_data)}")

        sqlite_tabledata = SQLiteTableDataSanitizer(
            table_data, max_workers=self.__max_workers
        ).normalize()
        self.__table_creator.create(
            sqlite_tabledata,
            self.__index_list,
            source_info=self.__source_info,
        )
        self.__converted_table_name_set.add(cast(str, sqlite_tabledata.table_name))
