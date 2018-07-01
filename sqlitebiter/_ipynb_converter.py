# encoding: utf-8

'''
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
'''

from __future__ import absolute_import, unicode_literals

import abc
import io
import json
import os.path
import re

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
        return nbformat.read(f, as_version=4)


def load_ipynb_url(url, proxies):
    response = requests.get(url, proxies=proxies)
    response.raise_for_status()

    return (nbformat.reads(response.text, as_version=4), len(response.content))


@six.add_metaclass(abc.ABCMeta)
class JupyterNotebookConverterInterface(object):

    @abc.abstractmethod
    def convert(self):  # pragma: no cover
        pass


class JupyterNotebookConverterBase(object):

    class Attr(object):
        CELL_ID = "cell_id"
        KEY = "key"
        LINE_NUMBER = "line_no"
        VALUE = "value"

    @abc.abstractproperty
    def _base_table_name(self):  # pragma: no cover
        pass

    def __init__(self, logger, con):
        self._logger = logger
        self._con = con

    def _make_table_name(self, name_list):
        return "_".join([self._base_table_name] + name_list)


class MetaDataConverter(JupyterNotebookConverterBase):

    @property
    def _base_table_name(self):
        return "metadata"

    def __init__(self, logger, con, metadata):
        super(MetaDataConverter, self).__init__(logger, con)

        self.__metadata = metadata

    def convert(self):
        if not self.__metadata:
            self._logger.debug("metadata not found")
            return

        self.__create_tables()
        self.__convert_kernelspec()
        self.__convert_language_info()
        self.__convert_kv()

        if self.__metadata:
            self._logger.debug("cannot convert: {}".format(json.dumps(self.__metadata, indent=4)))

    def __create_tables(self):
        self._con.create_table(
            self._make_table_name(["kernelspec"]),
            [
                "{:s} TEXT NOT NULL".format(self.Attr.KEY),
                "{:s} TEXT NOT NULL".format(self.Attr.VALUE),
            ])
        self._con.create_table(
            self._make_table_name(["language_info"]),
            [
                "{:s} TEXT NOT NULL".format(self.Attr.KEY),
                "{:s} TEXT NOT NULL".format(self.Attr.VALUE),
            ])
        self._con.create_table(
            self._make_table_name([KEY_VALUE_TABLE]),
            [
                "{:s} TEXT NOT NULL".format(self.Attr.KEY),
                "{:s} TEXT NOT NULL".format(self.Attr.VALUE),
            ])

    def __convert_kernelspec(self):
        target = "kernelspec"
        table_name = self._make_table_name([target])
        self._con.insert_many(
            table_name,
            [
                [key, value] for key, value in self.__metadata.get(target).items()
            ])

        del self.__metadata[target]

    def __convert_language_info(self):
        target = "language_info"
        language_info = self.__metadata.get(target)
        record_list = []

        codemirror_mode = language_info.get("codemirror_mode")
        if isinstance(codemirror_mode, dict):
            for key, value in codemirror_mode.items():
                record_list.append(("codemirror_mode_{:s}".format(key), value))
            del language_info["codemirror_mode"]

        for key, value in language_info.items():
            record_list.append((key, value))

        self._con.insert_many(self._make_table_name([target]), record_list)

        del self.__metadata[target]

    def __convert_kv(self):
        table_name = self._make_table_name([KEY_VALUE_TABLE])

        target = "anaconda-cloud"
        if target in self.__metadata:
            self._con.insert_many(
                table_name,
                [
                    [key, value] for key, value in self.__metadata.get(target).items()
                ])

            del self.__metadata[target]


class CellConverter(JupyterNotebookConverterBase):

    @property
    def _base_table_name(self):
        return "cells"

    def __init__(self, logger, con, cells):
        super(CellConverter, self).__init__(logger, con)

        self.__cells = cells
        self._cell_id = None

    def convert(self):
        self.__create_tables()

        for cell_id, cell_data in enumerate(self.__cells):
            self._cell_id = cell_id
            self.__convert_cell(cell_data)

    def __create_tables(self):
        self._con.create_table(
            self._make_table_name(["source"]),
            [
                "{:s} INTEGER NOT NULL".format(self.Attr.CELL_ID),
                "{:s} INTEGER NOT NULL".format(self.Attr.LINE_NUMBER),
                "{:s} TEXT".format("text"),
            ])
        self._con.create_table(
            self._make_table_name(["outputs"]),
            [
                "{:s} INTEGER NOT NULL".format(self.Attr.CELL_ID),
                "type TEXT NOT NULL",
                "{:s} INTEGER".format(self.Attr.LINE_NUMBER),
                "{:s} BLOB".format("data"),
            ])
        self._con.create_table(
            self._make_table_name(["outputs", KEY_VALUE_TABLE]),
            [
                "{:s} INTEGER NOT NULL".format(self.Attr.CELL_ID),
                "{:s} TEXT NOT NULL".format(self.Attr.KEY),
                "{:s} TEXT".format(self.Attr.VALUE),
            ])
        self._con.create_table(
            self._make_table_name([KEY_VALUE_TABLE]),
            [
                "{:s} INTEGER NOT NULL".format(self.Attr.CELL_ID),
                "{:s} TEXT NOT NULL".format(self.Attr.KEY),
                "{:s} TEXT".format(self.Attr.VALUE),
            ])

    def __convert_source(self, cell_data):
        target = "source"

        self._con.insert_many(
            self._make_table_name([target]),
            [
                [self._cell_id, line_no, source_line.rstrip()]
                for line_no, source_line in enumerate(cell_data.get(target).splitlines())
            ])

        del cell_data[target]

    def __to_kv_record_list(self, data_map):
        record_list = []
        for key, value in data_map.items():
            if key == "metadata":
                if not value:
                    record = (self._cell_id, key, None)
                else:
                    record = (self._cell_id, key, six.text_type(dict(value)))

                record_list.append(record)
                continue

            record_list.append((self._cell_id, key, value))

        return record_list

    def __convert_cell(self, cell_data):
        self._logger.debug("converting cell #{}".format(self._cell_id))

        self.__convert_source(cell_data)

        category = "outputs"
        if category in cell_data:
            for output_data in cell_data.outputs:
                self.__convert_output_text(output_data)
                self.__convert_output_data(output_data)

                self._con.insert_many(
                    self._make_table_name([category, KEY_VALUE_TABLE]),
                    self.__to_kv_record_list(output_data))

            del cell_data[category]

        self._con.insert_many(
            self._make_table_name([KEY_VALUE_TABLE]), self.__to_kv_record_list(cell_data))

    def __convert_output_text(self, output_data):
        data_type = "text"
        if data_type not in output_data:
            return

        self._con.insert_many(
            self._make_table_name(["outputs"]),
            [
                [self._cell_id, data_type, line_no, line]
                for line_no, line in enumerate(output_data.get(data_type).splitlines())
            ])

        del output_data[data_type]

    def __convert_output_data(self, output_data):
        output_key = "data"
        if output_key not in output_data:
            return

        table_name = self._make_table_name(["outputs"])
        image_regexp = re.compile("^image/.+")

        for data_type, data in output_data.get(output_key).items():
            self._logger.debug("table={} id={} data_type={} {}".format(
                table_name, self._cell_id, data_type, type(data)))

            if image_regexp.search(data_type):
                self._con.insert(table_name, [self._cell_id, data_type, 0, data])
                continue

            if isinstance(data, dict):
                data = json.dumps(data, indent=4)

            self._con.insert_many(
                table_name,
                [
                    [self._cell_id, data_type, data_no, line]
                    for data_no, line in enumerate(data.splitlines())
                ])

        del output_data[output_key]


def convert_nb(logger, con, result_counter, nb):
    CellConverter(logger, con, nb.cells).convert()
    MetaDataConverter(logger, con, nb.metadata).convert()

    table_name = KEY_VALUE_TABLE
    con.create_table(
        table_name,
        [
            "{:s} TEXT NOT NULL".format("key"),
            "{:s} TEXT".format("value"),
        ])
    con.insert_many(
        table_name,
        [
            [key, nb.get(key)] for key in ("nbformat", "nbformat_minor")
        ])
