#!/usr/bin/env python
# encoding: utf-8


"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""


from __future__ import absolute_import
import collections
import re

import click
import dataproperty
import path
import simplesqlite
from simplesqlite.loader import ValidationError
from simplesqlite.loader import InvalidDataError


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


class LoaderNotFound(Exception):
    pass


class LoaderFactory(object):
    LoaderTuple = collections.namedtuple(
        "LoaderTuple", "filename_regexp loader")

    LOADERTUPLE_LIST = [
        LoaderTuple(
            re.compile("[\.]csv$"),
            simplesqlite.loader.CsvTableFileLoader()),
        LoaderTuple(
            re.compile("[\.]json$"),
            simplesqlite.loader.JsonTableFileLoader()),
        LoaderTuple(
            re.compile("[\.]xlsx$|[\.]xlsm$|[\.]xls$"),
            simplesqlite.loader.ExcelTableFileLoader()),
    ]

    @classmethod
    def get_loader(cls, file_path):
        for loadertuple in cls.LOADERTUPLE_LIST:
            if loadertuple.filename_regexp.search(file_path) is None:
                continue

            loadertuple.loader.source = file_path

            return loadertuple.loader

        raise LoaderNotFound(file_path)


def create_database(database_path):
    db_path = path.Path(database_path)
    dir_path = db_path.dirname()
    if dataproperty.is_not_empty_string(dir_path):
        dir_path.makedirs_p()

    return simplesqlite.SimpleSQLite(db_path, "w")


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
def cmd():
    pass


@cmd.command()
@click.argument("files", type=str, nargs=-1)
@click.option(
    "-o", "--output-path", default="out.sqlite",
    help="Output path of the SQLite database file")
def file(files, output_path):
    """
    Convert CSV/JSON/Excel file(s) to a SQLite database file.
    """

    con = create_database(output_path)

    convert_count = 0
    for file_path in files:
        if not path.Path(file_path).isfile():
            continue

        try:
            loader = LoaderFactory.get_loader(file_path)
        except LoaderNotFound:
            continue

        try:
            for tabledata in loader.load():
                click.echo("convert '%s' to '%s' table" % (
                    file_path, tabledata.table_name))
                con.create_table_from_tabledata(tabledata)
            convert_count += 1
        except (ValueError, ValidationError, InvalidDataError):
            continue

    return 0 if convert_count == 0 else 1


@cmd.command()
@click.argument(
    "credentials", type=click.Path(exists=True))
@click.argument(
    "title", type=str)
@click.option(
    "-o", "--output-path", default="out.sqlite",
    help="output path of the SQLite database file")
def gs(credentials, title, output_path):
    """
    Convert Google Sheets to a SQLite database file.

    CREDENTIALS: OAuth2 Google credentials file.
    TITLE: Title of the Google Sheets to convert.
    """

    con = create_database(output_path)

    loader = simplesqlite.loader.GoogleSheetsTableLoader()
    loader.source = credentials
    loader.title = title

    for tabledata in loader.load():
        click.echo(
            "convert '%s' to '%s' table" % (title, tabledata.table_name))
        con.create_table_from_tabledata(tabledata)

    return 0


if __name__ == '__main__':
    cmd()
