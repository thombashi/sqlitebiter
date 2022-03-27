"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import os
import stat
from copy import deepcopy
from errno import EBADF, ENAMETOOLONG, ENOENT, ENOTDIR
from typing import Optional, Sequence

import msgfy
import pytablereader as ptr
from dataproperty import MatrixFormatting
from path import Path
from simplesqlite import SimpleSQLite

from .._const import IPYNB_FORMAT_NAME_LIST, TABLE_NOT_FOUND_MSG_FORMAT
from ._base import SourceInfo, TableConverter
from ._common import TYPE_HINT_FROM_HEADER_RULES
from ._ipynb_converter import is_ipynb_file_path, load_ipynb_file


def _get_format_type_from_path(file_path) -> str:
    return file_path.ext.lstrip(".")


class FileConverter(TableConverter):
    SKIP_MSG_FORMAT = "skip '{source:s}': {message:s}"

    def __init__(
        self,
        logger,
        con: SimpleSQLite,
        symbol_replace_value: Optional[str],
        add_pri_key_name: Optional[str],
        convert_configs,
        index_list: Sequence[str],
        is_type_inference: bool,
        is_type_hint_header: bool,
        matrix_formatting: MatrixFormatting,
        verbosity_level: int,
        max_workers: int,
        format_name,
        encoding,
        exclude_pattern,
        follow_symlinks,
    ):
        super().__init__(
            logger,
            con=con,
            symbol_replace_value=symbol_replace_value,
            add_pri_key_name=add_pri_key_name,
            convert_configs=convert_configs,
            index_list=index_list,
            is_type_inference=is_type_inference,
            is_type_hint_header=is_type_hint_header,
            matrix_formatting=matrix_formatting,
            verbosity_level=verbosity_level,
            max_workers=max_workers,
            format_name=format_name,
            encoding=encoding,
        )

        self.__exclude_pattern = exclude_pattern
        self.__follow_symlinks = follow_symlinks

    def convert(self, file_path) -> None:
        file_path = Path(file_path)
        logger = self._logger
        result_counter = self._result_counter

        if not self.__is_file(file_path):
            return

        if self.__exclude_pattern and file_path.fnmatch(self.__exclude_pattern):
            logger.debug(
                self.SKIP_MSG_FORMAT.format(source=file_path, message="matching an exclude pattern")
            )
            self._result_counter.inc_skip()
            return

        logger.debug(f"converting '{file_path}'")
        success_count = result_counter.success_count
        fail_count = result_counter.fail_count
        source_info_record_base = self.__get_source_info_base(file_path.realpath())

        if self._format_name in IPYNB_FORMAT_NAME_LIST or is_ipynb_file_path(file_path):
            import nbformat

            try:
                changed_table_name_set = self._convert_nb(
                    nb=load_ipynb_file(file_path, encoding=self._encoding),
                    source_info=source_info_record_base,
                )
            except (nbformat.reader.NotJSONError, RuntimeError) as e:
                logger.error(f"failed to load {file_path}: {e}")
                return

            for table_name in changed_table_name_set:
                record = deepcopy(source_info_record_base)
                record.format_name = "ipynb"
                record.dst_table = table_name
                SourceInfo.insert(record)
        else:
            self.__convert(file_path, source_info_record_base)

        if result_counter.fail_count > fail_count:
            return

        if result_counter.success_count == success_count:
            logger.warning(TABLE_NOT_FOUND_MSG_FORMAT.format(file_path))

    def __convert(self, file_path: Path, source_info_record_base: SourceInfo) -> None:
        logger = self._logger
        result_counter = self._result_counter

        try:
            loader = ptr.TableFileLoader(
                file_path,
                format_name=self._format_name,
                encoding=self._encoding,
                type_hint_rules=TYPE_HINT_FROM_HEADER_RULES if self._is_type_hint_header else None,
            )
        except ptr.InvalidFilePathError as e:
            logger.debug(msgfy.to_debug_message(e))
            result_counter.inc_fail()
            return
        except ptr.LoaderNotFoundError:
            logger.warning(f"not supported file format: ext={file_path.ext}, path={file_path}")
            result_counter.inc_fail()
            return

        source_info_record_base.format_name = loader.format_name

        try:
            for table_data in loader.load():
                logger.debug(f"loaded tabledata: {str(table_data)}")

                sqlite_tabledata = self.normalize_table(table_data)

                try:
                    self._table_creator.create(
                        sqlite_tabledata, self._index_list, source_info=source_info_record_base
                    )
                except (ValueError, OSError) as e:
                    logger.debug(f"exception={type(e).__name__:s}, path={file_path}, message={e}")
                    result_counter.inc_fail()
                    return

                record = deepcopy(source_info_record_base)
                record.dst_table = sqlite_tabledata.table_name
                SourceInfo.insert(record)
        except ptr.OpenError as e:
            logger.error(
                "{:s}: open error: file={}, message='{}'".format(
                    e.__class__.__name__, file_path, str(e)
                )
            )
            result_counter.inc_fail()
        except ptr.ValidationError as e:
            if loader.format_name == "json":
                for table_name in self._convert_complex_json(
                    loader.loader, source_info_record_base
                ):
                    record = deepcopy(source_info_record_base)
                    record.dst_table = table_name
                    SourceInfo.insert(record)
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
        except OverflowError as e:
            logger.error(f"{file_path}: {e}")
            result_counter.inc_fail()

    def __is_fifo(self, file_path: Path) -> bool:
        try:
            return stat.S_ISFIFO(os.stat(file_path).st_mode)
        except OSError as e:
            if e.errno not in (EBADF, ENAMETOOLONG, ENOENT, ENOTDIR):
                raise

            return False
        except ValueError:
            return False

    def __is_file(self, file_path: Path) -> bool:
        if not file_path.exists():
            self._logger.warning(
                self.SKIP_MSG_FORMAT.format(source=file_path, message="no such file or directory")
            )
            self._result_counter.inc_skip()
            return False

        if file_path.islink() and not self.__follow_symlinks:
            self._logger.info(
                self.SKIP_MSG_FORMAT.format(source=file_path, message="skip a symlink to a file")
            )
            self._result_counter.inc_skip()
            return False

        if not file_path.isfile() and not self.__is_fifo(file_path):
            self._logger.warning(
                self.SKIP_MSG_FORMAT.format(source=file_path, message="not a file")
            )
            self._result_counter.inc_skip()
            return False

        if file_path.realpath() == self._con.database_path:
            self._logger.warning(
                self.SKIP_MSG_FORMAT.format(
                    source=file_path, message="same path as the output file"
                )
            )
            self._result_counter.inc_skip()
            return False

        return True

    def __get_source_info_base(self, source: Path) -> SourceInfo:
        return SourceInfo(
            dir_name=source.dirname(),
            base_name=source.basename(),
            size=source.getsize(),
            mtime=int(source.getmtime()),
            source_id=self._fetch_next_source_id(),
        )
