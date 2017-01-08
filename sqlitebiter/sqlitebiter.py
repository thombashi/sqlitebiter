#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import sys

import click
import dataproperty
import logbook
import path
import pytablereader as ptr
import simplesqlite
from sqliteschema import SqliteSchemaExtractor

from ._counter import ResultCounter
from ._enum import (
    Context,
    ExitCode,
)
from ._version import VERSION


CONTEXT_SETTINGS = dict(
    help_option_names=["-h", "--help"],
    obj={},
)
MAX_VERBOSITY_LEVEL = 2
QUIET_LOG_LEVEL = logbook.NOTSET

logbook.StderrHandler(
    level=logbook.DEBUG,
    format_string='[{record.level_name}] {record.message}').push_application()


def create_database(ctx, database_path):
    is_append_table = ctx.obj.get(Context.IS_APPEND_TABLE)

    db_path = path.Path(database_path)
    dir_path = db_path.dirname()
    if dataproperty.is_not_empty_string(dir_path):
        dir_path.makedirs_p()

    if is_append_table:
        return simplesqlite.SimpleSQLite(db_path, "a")
    else:
        return simplesqlite.SimpleSQLite(db_path, "w")


def write_completion_message(logger, database_path, result_counter):
    logger.debug(u"----- sqlitebiter completed -----")
    logger.debug(u"database path: {:s}".format(database_path))
    logger.debug(u"number of created table: {:d}".format(
        result_counter.success_count))
    logger.debug(u"")

    logger.debug(u"----- database schema -----")
    logger.debug(
        get_schema_extractor(database_path, MAX_VERBOSITY_LEVEL).dumps())


def _setup_logger(logger, log_level):
    if log_level == QUIET_LOG_LEVEL:
        logger.disable()
        ptr.logger.disable()

    logger.level = log_level
    ptr.logger.level = log_level


def _get_format_type_from_path(file_path):
    return file_path.ext.lstrip(".")


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=VERSION)
@click.option(
    "--append", "is_append_table", is_flag=True,
    help="append table(s) to existing database.")
@click.option("-v", "--verbose", "verbosity_level", count=True)
@click.option(
    "--debug", "log_level", flag_value=logbook.DEBUG,
    help="for debug print.")
@click.option(
    "--quiet", "log_level", flag_value=QUIET_LOG_LEVEL,
    help="suppress execution log messages.")
@click.pass_context
def cmd(ctx, is_append_table, verbosity_level, log_level):
    ctx.obj[Context.IS_APPEND_TABLE] = is_append_table
    ctx.obj[Context.VERBOSITY_LEVEL] = verbosity_level
    ctx.obj[Context.LOG_LEVEL] = (
        logbook.INFO if log_level is None else log_level)


def get_schema_extractor(source, verbosity_level):
    if verbosity_level >= MAX_VERBOSITY_LEVEL:
        return SqliteSchemaExtractor(
            source, verbosity_level=0, output_format="table")

    if verbosity_level >= 1:
        return SqliteSchemaExtractor(
            source, verbosity_level=3, output_format="text")

    if verbosity_level == 0:
        return SqliteSchemaExtractor(
            source, verbosity_level=0, output_format="text")

    raise ValueError("invalid verbosity_level: {}".format(verbosity_level))


def get_success_log_format(verbosity_level):
    if verbosity_level <= 1:
        return u"convert '{:s}' to '{:s}' table"

    return u"convert '{:s}' to {:s}"


@cmd.command()
@click.argument("files", type=str, nargs=-1)
@click.option(
    "-o", "--output-path", metavar="PATH", default="out.sqlite",
    help="Output path of the SQLite database file")
@click.pass_context
def file(ctx, files, output_path):
    """
    Convert tabular data within CSV/Excel/HTML/JSON/LTSV/Markdown/TSV file(s)
    to a SQLite database file.
    """

    if dataproperty.is_empty_sequence(files):
        sys.exit(ExitCode.NO_INPUT)

    con = create_database(ctx, output_path)
    verbosity_level = ctx.obj.get(Context.VERBOSITY_LEVEL)
    extractor = get_schema_extractor(con, verbosity_level)
    result_counter = ResultCounter()

    logger = logbook.Logger("sqlitebiter file")
    _setup_logger(logger, ctx.obj[Context.LOG_LEVEL])

    for file_path in files:
        file_path = path.Path(file_path)
        if not file_path.isfile():
            logger.debug(u"file not found: {}".format(file_path))
            result_counter.inc_fail()
            continue

        logger.debug(u"converting '{}'".format(file_path))

        try:
            loader = ptr.TableFileLoader(file_path)
        except ptr.InvalidFilePathError as e:
            logger.debug(e)
            result_counter.inc_fail()
            continue
        except ptr.LoaderNotFoundError:
            logger.debug(
                u"loader not found that coincide with '{}'".format(file_path))
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
                        u"path={}, message={}".format(file_path, e))
                    result_counter.inc_fail()
                    continue

                log_message = get_success_log_format(verbosity_level).format(
                    file_path,
                    extractor.get_table_schema_text(sqlite_tabledata.table_name).strip())
                logger.info(log_message)
        except ptr.OpenError as e:
            logger.error(u"open error: file={}, message='{}'".format(
                file_path, str(e)))
            result_counter.inc_fail()
        except ptr.ValidationError as e:
            logger.error(
                u"invalid {} data format: path={}, message={}".format(
                    _get_format_type_from_path(file_path), file_path, str(e)))
            result_counter.inc_fail()
        except ptr.InvalidDataError as e:
            logger.error(
                u"invalid {} data: path={}, message={}".format(
                    _get_format_type_from_path(file_path), file_path, str(e)))
            result_counter.inc_fail()

    write_completion_message(logger, output_path, result_counter)

    sys.exit(result_counter.get_return_code())


@cmd.command()
@click.argument("url", type=str)
@click.option(
    "--format", "format_name",
    type=click.Choice(ptr.TableUrlLoader.get_format_name_list()),
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
    Scrape tabular data from a URL and convert data to a SQLite database file.
    """

    if dataproperty.is_empty_sequence(url):
        sys.exit(ExitCode.NO_INPUT)

    con = create_database(ctx, output_path)
    verbosity_level = ctx.obj.get(Context.VERBOSITY_LEVEL)
    extractor = get_schema_extractor(con, verbosity_level)
    result_counter = ResultCounter()

    logger = logbook.Logger("sqlitebiter url")
    _setup_logger(logger, ctx.obj[Context.LOG_LEVEL])

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
                    u"url={}, message={}".format(url, str(e)))
                result_counter.inc_fail()
                continue

            log_message = get_success_log_format(verbosity_level).format(
                url,
                extractor.get_table_schema_text(sqlite_tabledata.table_name).strip())
            logger.info(log_message)
    except ptr.InvalidDataError as e:
        logger.error(u"invalid data: url={}, message={}".format(url, str(e)))
        result_counter.inc_fail()

    write_completion_message(logger, output_path, result_counter)

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

    con = create_database(ctx, output_path)
    result_counter = ResultCounter()

    logger = logbook.Logger("sqlitebiter gs")
    _setup_logger(logger, ctx.obj[Context.LOG_LEVEL])

    loader = simplesqlite.loader.GoogleSheetsTableLoader()
    loader.source = credentials
    loader.title = title

    try:
        for tabledata in loader.load():
            click.echo(u"convert '{:s}' to '{:s}' table".format(
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
        logger.error(u"invalid credentials data: path={}".format(credentials))
        result_counter.inc_fail()
    except (ptr.ValidationError, ptr.InvalidDataError) as e:
        logger.error(
            u"invalid credentials data: path={}, message={}".format(
                credentials, str(e)))
        result_counter.inc_fail()

    write_completion_message(logger, output_path, result_counter)

    sys.exit(result_counter.get_return_code())


if __name__ == '__main__':
    cmd()
