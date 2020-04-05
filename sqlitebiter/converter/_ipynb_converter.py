"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import abc
import os.path
import re
from typing import TYPE_CHECKING, Dict, List, Optional, Sequence, Set, Tuple
from urllib.parse import urlparse

import msgfy
import nbformat
import retryrequests
import simplejson as json
from simplesqlite import SimpleSQLite

from .._common import ResultLogger


if TYPE_CHECKING:
    from ._base import SourceInfo  # noqa


KEY_VALUE_TABLE = "kv"


def is_ipynb_file_path(file_path: str) -> bool:
    return urlparse(file_path).scheme == "" and os.path.splitext(file_path)[1] == ".ipynb"


def is_ipynb_url(url: str) -> bool:
    result = urlparse(url)

    return result.scheme != "" and is_ipynb_file_path(result.path)


def _schema_not_found_error_handler(e: Exception) -> None:
    if re.search("No such file or directory: .+schema.json", str(e)):
        raise RuntimeError(
            "ipynb file format conversion not supported for the binary version. "
            "please try to install sqlitebiter via pip."
        )


def load_ipynb_file(file_path: str, encoding: str):
    with open(file_path, encoding=encoding) as f:
        try:
            return nbformat.read(f, as_version=4)
        except AttributeError as e:
            raise nbformat.reader.NotJSONError(msgfy.to_error_message(e))
        except OSError as e:
            _schema_not_found_error_handler(e)
            raise


def load_ipynb_text(text: str):
    try:
        return nbformat.reads(text, as_version=4)
    except AttributeError as e:
        raise nbformat.reader.NotJSONError(msgfy.to_error_message(e))
    except OSError as e:
        _schema_not_found_error_handler(e)
        raise


def load_ipynb_url(url: str, proxies: Optional[Dict]) -> Tuple:
    response = retryrequests.get(url, proxies=proxies)
    response.raise_for_status()

    try:
        return (nbformat.reads(response.text, as_version=4), len(response.content))
    except OSError as e:
        _schema_not_found_error_handler(e)
        raise


class NbAttr:
    CELL_ID = "cell_id"
    KEY = "key"
    LINE_NUMBER = "line_no"
    SOURECE_ID = "source_id"
    VALUE = "value"


class NbAttrDesc:
    CELL_ID = "{:s} INTEGER NOT NULL".format(NbAttr.CELL_ID)
    KEY = "{:s} TEXT NOT NULL".format(NbAttr.KEY)
    LINE_NUMBER = "{:s} INTEGER NOT NULL".format(NbAttr.LINE_NUMBER)
    SOURECE_ID = "{:s} INTEGER NOT NULL".format(NbAttr.SOURECE_ID)
    VALUE = "{:s} TEXT".format(NbAttr.VALUE)


class JupyterNotebookConverterInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def convert(self):  # pragma: no cover
        pass


class JupyterNotebookConverterBase(JupyterNotebookConverterInterface):
    @abc.abstractproperty
    def _base_table_name(self) -> str:  # pragma: no cover
        pass

    @property
    def source_id(self):
        return self._source_info.source_id

    def __init__(
        self, logger, source_info: "SourceInfo", con: SimpleSQLite, result_logger: ResultLogger
    ):
        self._logger = logger
        self._source_info = source_info
        self._con = con
        self._result_logger = result_logger
        self._changed_table_name_set = set()  # type: Set[str]

    def _get_log_header(self, info_name: str) -> str:
        return "{:s}: {:s}({:s})".format(
            self._source_info.get_name(self._result_logger.verbosity_level),
            self._base_table_name,
            info_name,
        )

    def _need_create_table(self, table_name: str) -> bool:
        return not self._con.has_table(table_name)

    def _make_table_name(self, names: List[str]) -> Tuple[str, bool]:
        table_name = "_".join([self._base_table_name] + names)

        return (table_name, self._need_create_table(table_name))


class MetaDataConverter(JupyterNotebookConverterBase):
    @property
    def _base_table_name(self):
        return "metadata"

    def __init__(
        self,
        logger,
        source_info: "SourceInfo",
        con: SimpleSQLite,
        result_logger: ResultLogger,
        metadata,
    ):
        super().__init__(logger, source_info, con, result_logger)

        self.__metadata = metadata

    def convert(self) -> Set[str]:
        if not self.__metadata:
            self._logger.debug("metadata not found")
            return set()

        self.__convert_kernelspec()
        self.__convert_language_info()
        self.__convert_kv()

        if self.__metadata:
            self._logger.debug(
                "cannot convert: {}".format(
                    json.dumps(self.__metadata, indent=4, ensure_ascii=False)
                )
            )

        return self._changed_table_name_set

    def __convert_kernelspec(self) -> None:
        target = "kernelspec"
        table_name, need_create_table = self._make_table_name([target])
        records = [
            [self.source_id, key, value] for key, value in self.__metadata.get(target).items()
        ]

        if len(records) > 0:
            self._con.create_table(
                table_name,
                [NbAttrDesc.SOURECE_ID, NbAttrDesc.KEY, "{:s} TEXT NOT NULL".format(NbAttr.VALUE)],
            )
            self._con.insert_many(table_name, records)

            self._result_logger.logging_success(
                self._get_log_header(target), table_name, need_create_table
            )
            self._changed_table_name_set.add(table_name)

        del self.__metadata[target]

    def __convert_language_info(self) -> None:
        target = "language_info"
        language_info = self.__metadata.get(target)
        record_list = []

        codemirror_mode = language_info.get("codemirror_mode")
        if isinstance(codemirror_mode, dict):
            for key, value in codemirror_mode.items():
                record_list.append((self.source_id, "codemirror_mode_{:s}".format(key), value))
            del language_info["codemirror_mode"]

        for key, value in language_info.items():
            record_list.append((self.source_id, key, value))

        table_name, need_create_table = self._make_table_name([target])
        if len(record_list) > 0:
            self._con.create_table(
                table_name,
                [NbAttrDesc.SOURECE_ID, NbAttrDesc.KEY, "{:s} TEXT NOT NULL".format(NbAttr.VALUE)],
            )
            self._con.insert_many(table_name, record_list)

            self._result_logger.logging_success(
                self._get_log_header(target), table_name, need_create_table
            )
            self._changed_table_name_set.add(table_name)

        del self.__metadata[target]

    def __convert_kv(self) -> None:
        target = "anaconda-cloud"

        if target in self.__metadata:
            table_name, need_create_table = self._make_table_name([KEY_VALUE_TABLE])
            records = [
                [self.source_id, key, value] for key, value in self.__metadata.get(target).items()
            ]

            if len(records) > 0:
                self._con.create_table(
                    table_name,
                    [
                        NbAttrDesc.SOURECE_ID,
                        NbAttrDesc.KEY,
                        "{:s} TEXT NOT NULL".format(NbAttr.VALUE),
                    ],
                )
                self._con.insert_many(table_name, records)

                self._result_logger.logging_success(
                    self._get_log_header(target), table_name, need_create_table
                )
                self._changed_table_name_set.add(table_name)

            del self.__metadata[target]


class CellConverter(JupyterNotebookConverterBase):
    @property
    def _base_table_name(self) -> str:
        return "cells"

    def __init__(
        self,
        logger,
        source_info: "SourceInfo",
        con: SimpleSQLite,
        result_logger: ResultLogger,
        cells: Sequence,
    ):
        super().__init__(logger, source_info, con, result_logger)

        self.__cells = cells
        self._cell_id = None  # type: Optional[int]

    def convert(self) -> Set[str]:
        for cell_id, cell_data in enumerate(self.__cells):
            self._cell_id = cell_id
            self.__convert_cell(cell_data)

        return self._changed_table_name_set

    def _get_log_header(self, info_name: str) -> str:
        return "{:s}: {:s}#{}({:s})".format(
            self._source_info.base_name, self._base_table_name, self._cell_id, info_name
        )

    def __convert_source(self, cell_data: Dict[str, str]) -> None:
        target = "source"
        table_name, need_create_table = self._make_table_name([target])
        records = [
            [self.source_id, self._cell_id, line_no, source_line.rstrip()]
            for line_no, source_line in enumerate(cell_data[target].splitlines())
        ]

        del cell_data[target]

        if len(records) > 0:
            self._con.create_table(
                table_name,
                [
                    NbAttrDesc.SOURECE_ID,
                    NbAttrDesc.CELL_ID,
                    NbAttrDesc.LINE_NUMBER,
                    "{:s} TEXT".format("text"),
                ],
            )
            self._con.insert_many(table_name, records)

            self._result_logger.logging_success(
                self._get_log_header(target), table_name, need_create_table
            )
            self._changed_table_name_set.add(table_name)

    def __to_kv_records(self, data_map: Dict) -> List[Tuple]:
        record_list = []  # type: List[Tuple]
        for key, value in data_map.items():
            if key == "metadata":
                if not value:
                    record = (self.source_id, self._cell_id, key, None)
                else:
                    record = (self.source_id, self._cell_id, key, str(dict(value)))  # type: ignore

                record_list.append(record)
                continue

            record_list.append((self.source_id, self._cell_id, key, value))

        return record_list

    def __convert_cell(self, cell_data) -> None:
        self.__convert_source(cell_data)

        category = "outputs"
        if category in cell_data:
            outputs_table_name, need_create_output_table = self._make_table_name([category])
            self._con.create_table(
                outputs_table_name,
                [
                    NbAttrDesc.SOURECE_ID,
                    NbAttrDesc.CELL_ID,
                    "type TEXT NOT NULL",
                    NbAttrDesc.LINE_NUMBER,
                    "{:s} BLOB".format("data"),
                ],
            )

            outputs_kv_table_name, need_create_output_kv_table = self._make_table_name(
                [category, KEY_VALUE_TABLE]
            )
            self._con.create_table(
                outputs_kv_table_name,
                [NbAttrDesc.SOURECE_ID, NbAttrDesc.CELL_ID, NbAttrDesc.KEY, NbAttrDesc.VALUE],
            )

            for output_data in cell_data.outputs:
                if self.__convert_output_text(output_data, need_create_output_table):
                    need_create_output_table = False
                if self.__convert_output_data(output_data, need_create_output_table):
                    need_create_output_table = False

                self._con.insert_many(outputs_kv_table_name, self.__to_kv_records(output_data))
                self._result_logger.logging_success(
                    self._get_log_header("{} {}".format(category, KEY_VALUE_TABLE)),
                    outputs_kv_table_name,
                    need_create_output_kv_table,
                )
                self._changed_table_name_set.add(outputs_kv_table_name)
                need_create_output_kv_table = False

            del cell_data[category]

        if not cell_data:
            return

        kv_records = self.__to_kv_records(cell_data)
        if len(kv_records) == 0:
            return

        kv_table_name, need_create_kv_table = self._make_table_name([KEY_VALUE_TABLE])
        self._con.create_table(
            kv_table_name,
            [NbAttrDesc.SOURECE_ID, NbAttrDesc.CELL_ID, NbAttrDesc.KEY, NbAttrDesc.VALUE],
        )
        self._con.insert_many(kv_table_name, kv_records)

        self._result_logger.logging_success(
            self._get_log_header(KEY_VALUE_TABLE), kv_table_name, need_create_kv_table
        )
        self._changed_table_name_set.add(kv_table_name)

    def __convert_output_text(self, output_data, need_create_table: bool) -> bool:
        data_type = "text"
        if data_type not in output_data:
            return False

        table_name, _ = self._make_table_name(["outputs"])

        num_record = self._con.insert_many(
            table_name,
            [
                [self.source_id, self._cell_id, data_type, line_no, line]
                for line_no, line in enumerate(output_data.get(data_type).splitlines())
            ],
        )

        del output_data[data_type]

        if num_record == 0:
            return False

        self._result_logger.logging_success(
            self._get_log_header("outputs {}".format(data_type)), table_name, need_create_table
        )
        self._changed_table_name_set.add(table_name)

        return True

    def __convert_output_data(self, output_data: Dict[str, Dict], need_create_table: bool) -> bool:
        output_key = "data"
        if output_key not in output_data:
            return False

        table_name, _ = self._make_table_name(["outputs"])
        image_regexp = re.compile("^image/.+")
        num_record = 0

        for data_type, data in output_data[output_key].items():
            self._logger.debug(
                "table={} id={} data_type={} {}".format(
                    table_name, self._cell_id, data_type, type(data)
                )
            )

            if image_regexp.search(data_type):
                self._con.insert(table_name, [self.source_id, self._cell_id, data_type, 0, data])
                num_record += 1
                continue

            if isinstance(data, dict):
                data = json.dumps(data, indent=4, ensure_ascii=False)

            num_record += self._con.insert_many(
                table_name,
                [
                    [self.source_id, self._cell_id, data_type, data_no, line]
                    for data_no, line in enumerate(data.splitlines())
                ],
            )

        del output_data[output_key]

        if num_record == 0:
            return False

        self._result_logger.logging_success(
            self._get_log_header("outputs {}".format(data_type)), table_name, need_create_table
        )
        self._changed_table_name_set.add(table_name)

        return True


def convert_nb(
    logger, source_info: "SourceInfo", con: SimpleSQLite, result_logger: ResultLogger, nb
) -> Set[str]:
    changed_table_name_set = set()  # type: Set[str]
    changed_table_name_set |= CellConverter(
        logger, source_info, con, result_logger, nb.cells
    ).convert()
    changed_table_name_set |= MetaDataConverter(
        logger, source_info, con, result_logger, nb.metadata
    ).convert()

    table_name = KEY_VALUE_TABLE
    need_create_table = not con.has_table(table_name)
    kv_records = [
        [source_info.source_id, key, nb.get(key)] for key in ("nbformat", "nbformat_minor")
    ]

    if len(kv_records) > 0:
        con.create_table(table_name, [NbAttrDesc.SOURECE_ID, NbAttrDesc.KEY, NbAttrDesc.VALUE])
        con.insert_many(table_name, kv_records)

        result_logger.logging_success(
            "{}: {}".format(source_info.base_name, table_name), table_name, need_create_table
        )
        changed_table_name_set.add(table_name)

    con.commit()

    return changed_table_name_set
