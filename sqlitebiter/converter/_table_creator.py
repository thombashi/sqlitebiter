"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from textwrap import dedent
from typing import TYPE_CHECKING, Optional, Sequence

import simplesqlite
from simplesqlite import SimpleSQLite
from tabledata import TableData
from typepy import String

from .._common import ResultLogger


try:
    import ujson as json
except ImportError:
    import json  # type: ignore


if TYPE_CHECKING:
    from ._base import SourceInfo  # noqa


class TableCreator:
    def __init__(
        self,
        logger,
        dst_con: SimpleSQLite,
        add_pri_key_name: Optional[str],
        result_logger: ResultLogger,
        verbosity_level: int,
        max_workers: int,
    ) -> None:
        self.__logger = logger
        self.__dst_con = dst_con
        self.__add_pri_key_name = add_pri_key_name
        self.__result_logger = result_logger
        self.__verbosity_level = verbosity_level
        self.__max_workers = max_workers

    def create(
        self, table_data: TableData, index_list: Sequence[str], source_info: "SourceInfo"
    ) -> None:
        con_mem = simplesqlite.connect_memdb(max_workers=self.__max_workers)

        con_mem.create_table_from_tabledata(
            table_data,
            primary_key=self.__add_pri_key_name,
            add_primary_key_column=String(self.__add_pri_key_name).is_type(),
        )

        src_table_name = con_mem.fetch_table_names()[0]
        dst_table_name = src_table_name

        if self.__require_rename_table(con_mem, src_table_name):
            dst_table_name = self.__make_unique_table_name(src_table_name)

            self.__logger.debug(f"rename table from '{src_table_name}' to '{dst_table_name}'")

            is_create_table = True
            simplesqlite.copy_table(
                src_con=con_mem,
                dst_con=self.__dst_con,
                src_table_name=src_table_name,
                dst_table_name=dst_table_name,
            )
        else:
            is_create_table = not self.__dst_con.has_table(dst_table_name)
            simplesqlite.append_table(
                src_con=con_mem, dst_con=self.__dst_con, table_name=dst_table_name
            )

        self.__dst_con.create_index_list(dst_table_name, index_list)

        self.__result_logger.logging_success(
            source_info.get_name(self.__verbosity_level), dst_table_name, is_create_table
        )

    def __require_rename_table(self, src_con: SimpleSQLite, src_table_name: str) -> bool:
        if not self.__dst_con.has_table(src_table_name):
            return False

        lhs = self.__dst_con.schema_extractor.fetch_table_schema(src_table_name).as_dict()
        rhs = src_con.schema_extractor.fetch_table_schema(src_table_name).as_dict()

        if lhs != rhs:
            self.__logger.debug(
                dedent(
                    """\
                    require rename '{table}' because of src table and dst table has
                    a different schema with the same table name:
                    dst-schema={dst_schema}
                    src-schema={src_schema}
                    """
                ).format(
                    table=src_table_name,
                    src_schema=json.dumps(lhs, indent=4, ensure_ascii=False),
                    dst_schema=json.dumps(rhs, indent=4, ensure_ascii=False),
                )
            )
            return True

        return False

    def __make_unique_table_name(self, table_name_base: str) -> str:
        exist_table_names = self.__dst_con.fetch_table_names()

        if table_name_base not in exist_table_names:
            return table_name_base

        suffix_id = 1
        while True:
            table_name_candidate = f"{table_name_base:s}_{suffix_id:d}"

            if table_name_candidate not in exist_table_names:
                return table_name_candidate

            suffix_id += 1
