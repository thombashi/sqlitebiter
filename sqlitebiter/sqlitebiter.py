#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import sys

import click
import dataproperty
import logbook
import path
import pytablereader as ptr
import simplesqlite
from sqlitestructure import TableStructureWriter

from ._counter import ResultCounter
from ._enum import ExitCode


CONTEXT_SETTINGS = dict(
    help_option_names=["-h", "--help"],
    obj={},
)
SQLITE_TABLE_VERBOSE_LEVEL = 2

handler = logbook.StderrHandler()
handler.push_application()


def create_database(database_path):
    db_path = path.Path(database_path)
    dir_path = db_path.dirname()
    if dataproperty.is_not_empty_string(dir_path):
        dir_path.makedirs_p()

    return simplesqlite.SimpleSQLite(db_path, "w")


def _setup_logger_from_context(ctx, logger):
    log_level = ctx.obj.get("LOG_LEVEL")

    if log_level == logbook.NOTSET:
        logger.disable()
        ptr.logger.disable()
    elif log_level is None:
        log_level = logbook.INFO
        ptr.logger.level = logbook.INFO

    logger.level = log_level
    ptr.logger.level = log_level


def _get_format_type_from_path(file_path):
    return file_path.ext.lstrip(".")


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
@click.option(
    "--debug", "log_level", flag_value=logbook.DEBUG,
    help="for debug print.")
@click.option(
    "--quiet", "log_level", flag_value=logbook.NOTSET,
    help="suppress execution log messages.")
@click.pass_context
def cmd(ctx, log_level):
    ctx.obj["LOG_LEVEL"] = log_level


@cmd.command()
@click.argument("files", type=str, nargs=-1)
@click.option(
    "-o", "--output-path", metavar="PATH", default="out.sqlite",
    help="Output path of the SQLite database file")
@click.pass_context
def file(ctx, files, output_path):
    """
    Convert CSV/Excel/HTML/JSON/Markdown file(s) to a SQLite database file.
    """

    if dataproperty.is_empty_sequence(files):
        sys.exit(ExitCode.NO_INPUT)

    con = create_database(output_path)
    result_counter = ResultCounter()

    logger = logbook.Logger("sqlitebiter file")
    _setup_logger_from_context(ctx, logger)

    for file_path in files:
        file_path = path.Path(file_path)
        if not file_path.isfile():
            logger.debug("file not found: {}".format(file_path))
            result_counter.inc_fail()
            continue

        logger.debug("converting '{}'".format(file_path))

        try:
            loader = ptr.TableFileLoader(file_path)
        except ptr.InvalidFilePathError as e:
            logger.debug(e)
            result_counter.inc_fail()
            continue
        except ptr.LoaderNotFoundError:
            logger.debug(
                "loader not found that coincide with '{}'".format(file_path))
            result_counter.inc_fail()
            continue

        try:
            for tabledata in loader.load():
                sqlite_tabledata = ptr.SQLiteTableDataSanitizer(
                    tabledata).sanitize()

                try:
                    con.create_table_from_tabledata(sqlite_tabledata)
                    result_counter.inc_success()
                except (ValueError, IOError) as e:
                    logger.debug(
                        "path={}, message={}".format(file_path, e))
                    result_counter.inc_fail()
                    continue

                click.echo("convert '{:s}' to '{:s}' table".format(
                    file_path, sqlite_tabledata.table_name))
        except ptr.OpenError as e:
            logger.error("open error: file={}, message='{}'".format(
                file_path, str(e)))
            result_counter.inc_fail()
        except ptr.ValidationError as e:
            logger.error(
                "invalid {} data format: path={}, message={}".format(
                    _get_format_type_from_path(file_path), file_path, str(e)))
            result_counter.inc_fail()
        except ptr.InvalidDataError as e:
            logger.error(
                "invalid {} data: path={}, message={}".format(
                    _get_format_type_from_path(file_path), file_path, str(e)))
            result_counter.inc_fail()

    logger.debug(TableStructureWriter(
        output_path, SQLITE_TABLE_VERBOSE_LEVEL).dumps())

    sys.exit(result_counter.get_return_code())


@cmd.command()
@click.argument("url", type=str)
@click.option(
    "--format", "format_name",
    type=click.Choice(["csv", "excel", "html", "json", "markdown"]),
    help="Data format to loading (defaults to html).")
@click.option(
    "-o", "--output-path", metavar="PATH", default="out.sqlite",
    help="Output path of the SQLite database file.")
@click.option(
    "--encoding", type=str, metavar="ENCODING", default="utf-8",
    help="Defaults to utf-8")
@click.option(
    "--proxy", type=str, metavar="PROXY",
    help="Specify a proxy in the form [user:passwd@]proxy.server:port.")
@click.pass_context
def url(ctx, url, format_name, output_path, encoding, proxy):
    """
    Fetch data from a URL and convert data to a SQLite database file.
    """

    if dataproperty.is_empty_sequence(url):
        sys.exit(ExitCode.NO_INPUT)

    con = create_database(output_path)
    result_counter = ResultCounter()

    logger = logbook.Logger("sqlitebiter url")
    _setup_logger_from_context(ctx, logger)

    proxies = {}
    if dataproperty.is_not_empty_string(proxy):
        proxies = {
            "http": proxy,
            "https": proxy,
        }

    try:
        loader = ptr.TableUrlLoader(
            url, format_name, encoding=encoding, proxies=proxies)
    except ptr.LoaderNotFoundError as e:
        try:
            loader = ptr.TableUrlLoader(
                url, "html", encoding=encoding, proxies=proxies)
        except (ptr.LoaderNotFoundError, ptr.HTTPError):
            logger.error(e)
            sys.exit(ExitCode.FAILED_LOADER_NOT_FOUND)
    except ptr.HTTPError as e:
        logger.error(e)
        sys.exit(ExitCode.FAILED_HTTP)

    try:
        for tabledata in loader.load():
            sqlite_tabledata = ptr.SQLiteTableDataSanitizer(
                tabledata).sanitize()

            try:
                con.create_table_from_tabledata(sqlite_tabledata)
                result_counter.inc_success()
            except (ValueError) as e:
                logger.debug(
                    "url={}, message={}".format(url, str(e)))
                result_counter.inc_fail()
                continue

            click.echo("convert a table to '{:s}' table".format(
                sqlite_tabledata.table_name))
    except ptr.InvalidDataError as e:
        logger.error("invalid data: url={}, message={}".format(url, str(e)))
        result_counter.inc_fail()

    logger.debug(TableStructureWriter(
        output_path, SQLITE_TABLE_VERBOSE_LEVEL).dumps())

    sys.exit(result_counter.get_return_code())


@cmd.command()
@click.argument(
    "credentials", type=click.Path(exists=True))
@click.argument(
    "title", type=str)
@click.option(
    "-o", "--output-path", metavar="PATH", default="out.sqlite",
    help="output path of the SQLite database file")
@click.pass_context
def gs(ctx, credentials, title, output_path):
    """
    Convert Google Sheets to a SQLite database file.

    CREDENTIALS: OAuth2 Google credentials file.
    TITLE: Title of the Google Sheets to convert.
    """

    con = create_database(output_path)
    result_counter = ResultCounter()

    logger = logbook.Logger("sqlitebiter gs")
    _setup_logger_from_context(ctx, logger)

    loader = simplesqlite.loader.GoogleSheetsTableLoader()
    loader.source = credentials
    loader.title = title

    try:
        for tabledata in loader.load():
            click.echo("convert '{:s}' to '{:s}' table".format(
                title, tabledata.table_name))

            try:
                con.create_table_from_tabledata(tabledata)
                result_counter.inc_success()
            except (ptr.ValidationError, ptr.InvalidDataError):
                result_counter.inc_fail()
    except ptr.OpenError as e:
        logger.error(e)
        result_counter.inc_fail()
    except AttributeError:
        logger.error("invalid credentials data: path={}".format(credentials))
        result_counter.inc_fail()
    except (ptr.ValidationError, ptr.InvalidDataError) as e:
        logger.error(
            "invalid credentials data: path={}, message={}".format(
                credentials, str(e)))
        result_counter.inc_fail()

    logger.debug(TableStructureWriter(
        output_path, SQLITE_TABLE_VERBOSE_LEVEL).dumps())

    sys.exit(result_counter.get_return_code())


if __name__ == '__main__':
    cmd()
