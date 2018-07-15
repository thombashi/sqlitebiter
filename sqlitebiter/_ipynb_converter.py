# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import abc
import io
import json
import os.path
import re

import msgfy
import nbformat
import requests
import six
from six.moves.urllib.parse import urlparse


KEY_VALUE_TABLE = "kv"


def is_ipynb_file_path(file_path):
    return urlparse(file_path).scheme == "" and os.path.splitext(file_path)[1] == ".ipynb"


def is_ipynb_url(url):
    result = urlparse(url)

    return result.scheme != "" and is_ipynb_file_path(result.path)


def load_ipynb_file(file_path, encoding):
    with io.open(file_path, encoding=encoding) as f:
        try:
            return nbformat.read(f, as_version=4)
        except AttributeError as e:
            raise nbformat.reader.NotJSONError(msgfy.to_error_message(e))


def load_ipynb_url(url, proxies):
    response = requests.get(url, proxies=proxies)
    response.raise_for_status()

    return (nbformat.reads(response.text, as_version=4), len(response.content))


class NbAttr(object):
    CELL_ID = "cell_id"
    KEY = "key"
    LINE_NUMBER = "line_no"
    SOURECE_ID = "source_id"
    VALUE = "value"


class NbAttrDesc(object):
    SOURECE_ID = "{:s} INTEGER NOT NULL".format(NbAttr.SOURECE_ID)


@six.add_metaclass(abc.ABCMeta)
class JupyterNotebookConverterInterface(object):
    @abc.abstractmethod
    def convert(self):  # pragma: no cover
        pass


class JupyterNotebookConverterBase(JupyterNotebookConverterInterface):
    @abc.abstractproperty
    def _base_table_name(self):  # pragma: no cover
        pass

    @property
    def source_id(self):
        return self._source_info.source_id

    def __init__(self, logger, source_info, con, result_logger):
        self._logger = logger
        self._source_info = source_info
        self._con = con
        self._result_logger = result_logger

    def _get_log_header(self, info_name):
        return "{:s}: {:s}({:s})".format(
            self._source_info.base_name, self._base_table_name, info_name
        )

    def _need_create_table(self, table_name):
        return not self._con.has_table(table_name)

    def _make_table_name(self, name_list):
        table_name = "_".join([self._base_table_name] + name_list)

        return (table_name, self._need_create_table(table_name))


class MetaDataConverter(JupyterNotebookConverterBase):
    @property
    def _base_table_name(self):
        return "metadata"

    def __init__(self, logger, source_info, con, result_logger, metadata):
        super(MetaDataConverter, self).__init__(logger, source_info, con, result_logger)

        self.__metadata = metadata

    def convert(self):
        if not self.__metadata:
            self._logger.debug("metadata not found")
            return

        self.__convert_kernelspec()
        self.__convert_language_info()
        self.__convert_kv()

        if self.__metadata:
            self._logger.debug("cannot convert: {}".format(json.dumps(self.__metadata, indent=4)))

    def __convert_kernelspec(self):
        target = "kernelspec"
        table_name, need_create_table = self._make_table_name([target])
        record_list = [[key, value] for key, value in self.__metadata.get(target).items()]

        if len(record_list) > 0:
            self._con.create_table(
                table_name,
                [
                    NbAttrDesc.SOURECE_ID,
                    "{:s} TEXT NOT NULL".format(NbAttr.KEY),
                    "{:s} TEXT NOT NULL".format(NbAttr.VALUE),
                ],
            )
            self._con.insert_many(
                table_name,
                [
                    [self.source_id, key, value]
                    for key, value in self.__metadata.get(target).items()
                ],
            )

            self._result_logger.logging_success(
                self._get_log_header(target), table_name, need_create_table
            )

        del self.__metadata[target]

    def __convert_language_info(self):
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
                [
                    NbAttrDesc.SOURECE_ID,
                    "{:s} TEXT NOT NULL".format(NbAttr.KEY),
                    "{:s} TEXT NOT NULL".format(NbAttr.VALUE),
                ],
            )
            self._con.insert_many(table_name, record_list)

            self._result_logger.logging_success(
                self._get_log_header(target), table_name, need_create_table
            )

        del self.__metadata[target]

    def __convert_kv(self):
        target = "anaconda-cloud"

        if target in self.__metadata:
            table_name, need_create_table = self._make_table_name([KEY_VALUE_TABLE])
            record_list = [
                [self.source_id, key, value] for key, value in self.__metadata.get(target).items()
            ]

            if len(record_list) > 0:
                self._con.create_table(
                    table_name,
                    [
                        NbAttrDesc.SOURECE_ID,
                        "{:s} TEXT NOT NULL".format(NbAttr.KEY),
                        "{:s} TEXT NOT NULL".format(NbAttr.VALUE),
                    ],
                )
                self._con.insert_many(table_name, record_list)

                self._result_logger.logging_success(
                    self._get_log_header(target), table_name, need_create_table
                )

            del self.__metadata[target]


class CellConverter(JupyterNotebookConverterBase):
    @property
    def _base_table_name(self):
        return "cells"

    def __init__(self, logger, source_info, con, result_logger, cells):
        super(CellConverter, self).__init__(logger, source_info, con, result_logger)

        self.__cells = cells
        self._cell_id = None

    def convert(self):
        for cell_id, cell_data in enumerate(self.__cells):
            self._cell_id = cell_id
            self.__convert_cell(cell_data)

    def _get_log_header(self, info_name):
        return "{:s}: {:s}#{:d}({:s})".format(
            self._source_info.base_name, self._base_table_name, self._cell_id, info_name
        )

    def __convert_source(self, cell_data):
        target = "source"
        table_name, need_create_table = self._make_table_name([target])
        record_list = [
            [self.source_id, self._cell_id, line_no, source_line.rstrip()]
            for line_no, source_line in enumerate(cell_data.get(target).splitlines())
        ]

        del cell_data[target]

        if len(record_list) > 0:
            self._con.create_table(
                table_name,
                [
                    NbAttrDesc.SOURECE_ID,
                    "{:s} INTEGER NOT NULL".format(NbAttr.CELL_ID),
                    "{:s} INTEGER NOT NULL".format(NbAttr.LINE_NUMBER),
                    "{:s} TEXT".format("text"),
                ],
            )
            self._con.insert_many(table_name, record_list)

            self._result_logger.logging_success(
                self._get_log_header(target), table_name, need_create_table
            )

    def __to_kv_record_list(self, data_map):
        record_list = []
        for key, value in data_map.items():
            if key == "metadata":
                if not value:
                    record = (self.source_id, self._cell_id, key, None)
                else:
                    record = (self.source_id, self._cell_id, key, six.text_type(dict(value)))

                record_list.append(record)
                continue

            record_list.append((self.source_id, self._cell_id, key, value))

        return record_list

    def __convert_cell(self, cell_data):
        self.__convert_source(cell_data)

        category = "outputs"
        if category in cell_data:
            outputs_table_name, need_create_output_table = self._make_table_name([category])
            self._con.create_table(
                outputs_table_name,
                [
                    NbAttrDesc.SOURECE_ID,
                    "{:s} INTEGER NOT NULL".format(NbAttr.CELL_ID),
                    "type TEXT NOT NULL",
                    "{:s} INTEGER".format(NbAttr.LINE_NUMBER),
                    "{:s} BLOB".format("data"),
                ],
            )

            outputs_kv_table_name, need_create_output_kv_table = self._make_table_name(
                [category, KEY_VALUE_TABLE]
            )
            self._con.create_table(
                outputs_kv_table_name,
                [
                    NbAttrDesc.SOURECE_ID,
                    "{:s} INTEGER NOT NULL".format(NbAttr.CELL_ID),
                    "{:s} TEXT NOT NULL".format(NbAttr.KEY),
                    "{:s} TEXT".format(NbAttr.VALUE),
                ],
            )

            for output_data in cell_data.outputs:
                self.__convert_output_text(output_data, need_create_output_table)
                need_create_output_table = False
                self.__convert_output_data(output_data, need_create_output_table)

                self._con.insert_many(outputs_kv_table_name, self.__to_kv_record_list(output_data))
                self._result_logger.logging_success(
                    self._get_log_header("{} {}".format(category, KEY_VALUE_TABLE)),
                    outputs_kv_table_name,
                    need_create_output_kv_table,
                )
                need_create_output_kv_table = False

            del cell_data[category]

        if not cell_data:
            return

        kv_record_list = self.__to_kv_record_list(cell_data)
        if len(kv_record_list) == 0:
            return

        kv_table_name, need_create_kv_table = self._make_table_name([KEY_VALUE_TABLE])
        self._con.create_table(
            kv_table_name,
            [
                NbAttrDesc.SOURECE_ID,
                "{:s} INTEGER NOT NULL".format(NbAttr.CELL_ID),
                "{:s} TEXT NOT NULL".format(NbAttr.KEY),
                "{:s} TEXT".format(NbAttr.VALUE),
            ],
        )
        self._con.insert_many(kv_table_name, kv_record_list)

        self._result_logger.logging_success(
            self._get_log_header(KEY_VALUE_TABLE), kv_table_name, need_create_kv_table
        )

    def __convert_output_text(self, output_data, need_create_table):
        data_type = "text"
        if data_type not in output_data:
            return

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
            return

        self._result_logger.logging_success(
            self._get_log_header("outputs {}".format(data_type)), table_name, need_create_table
        )

    def __convert_output_data(self, output_data, need_create_table):
        output_key = "data"
        if output_key not in output_data:
            return

        table_name, _ = self._make_table_name(["outputs"])
        image_regexp = re.compile("^image/.+")
        num_record = 0

        for data_type, data in output_data.get(output_key).items():
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
                data = json.dumps(data, indent=4)

            num_record += self._con.insert_many(
                table_name,
                [
                    [self.source_id, self._cell_id, data_type, data_no, line]
                    for data_no, line in enumerate(data.splitlines())
                ],
            )

        del output_data[output_key]

        if num_record == 0:
            return

        self._result_logger.logging_success(
            self._get_log_header("outputs {}".format(data_type)), table_name, need_create_table
        )


def convert_nb(logger, source_info, con, result_logger, nb):
    existing_table_name_set = set(con.fetch_table_name_list())

    CellConverter(logger, source_info, con, result_logger, nb.cells).convert()
    MetaDataConverter(logger, source_info, con, result_logger, nb.metadata).convert()

    table_name = KEY_VALUE_TABLE
    need_create_table = not con.has_table(table_name)
    kv_record_list = [
        [source_info.source_id, key, nb.get(key)] for key in ("nbformat", "nbformat_minor")
    ]

    if len(kv_record_list) > 0:
        con.create_table(
            table_name,
            [
                NbAttrDesc.SOURECE_ID,
                "{:s} TEXT NOT NULL".format("key"),
                "{:s} TEXT".format("value"),
            ],
        )
        con.insert_many(table_name, kv_record_list)
        result_logger.logging_success(
            "{}: {}".format(source_info.base_name, table_name), table_name, need_create_table
        )

    con.commit()

    return set(con.fetch_table_name_list()) - existing_table_name_set
