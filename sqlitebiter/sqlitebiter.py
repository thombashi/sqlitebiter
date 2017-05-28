#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import errno
import sys

import click
import logbook
import path
import simplesqlite
from sqliteschema import SqliteSchemaExtractor
import typepy

import pytablereader as ptr

from ._config import (
    ConfigKey,
    app_config_manager,
)
from ._const import PROGRAM_NAME
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
    format_string="[{record.level_name}] {record.channel}: {record.message}"
).push_application()


class Default(object):
    OUTPUT_FILE = "out.sqlite"
    ENCODING = "utf-8"


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


def get_success_message(verbosity_level, source, to_table_name):
    message_template = u"convert '{:s}' to '{:s}' table"

    return message_template.format(source, to_table_name)


def create_database(ctx, database_path):
    is_append_table = ctx.obj.get(Context.IS_APPEND_TABLE)

    db_path = path.Path(database_path)
    dir_path = db_path.dirname()
    if typepy.is_not_null_string(dir_path):
        dir_path.makedirs_p()

    if is_append_table:
        return simplesqlite.SimpleSQLite(db_path, "a")
    else:
        return simplesqlite.SimpleSQLite(db_path, "w")


def write_completion_message(logger, database_path, result_counter):
    logger.debug(u"----- {:s} completed -----".format(PROGRAM_NAME))
    logger.debug(u"database path: {:s}".format(database_path))
    logger.debug(u"number of created table: {:d}".format(
        result_counter.success_count))
    logger.debug(u"")

    logger.debug(u"----- database schema -----")
    logger.debug(
        get_schema_extractor(database_path, MAX_VERBOSITY_LEVEL).dumps())


def make_logger(channel_name, log_level):
    import appconfigpy

    logger = logbook.Logger(channel_name)

    if log_level == QUIET_LOG_LEVEL:
        logger.disable()

    logger.level = log_level
    ptr.set_log_level(log_level)
    simplesqlite.set_log_level(log_level)
    appconfigpy.set_log_level(log_level)

    return logger


def create_url_loader(logger, url, format_name, encoding, proxies):
    try:
        return ptr.TableUrlLoader(
            url, format_name, encoding=encoding, proxies=proxies)
    except ptr.HTTPError as e:
        logger.error(e)
        sys.exit(ExitCode.FAILED_HTTP)
    except ptr.ProxyError as e:
        logger.error(e)
        sys.exit(errno.ECONNABORTED)


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


class TableCreator(object):

    def __init__(self, dst_con, tabledata):
        self.__dst_con = dst_con
        self.__tabledata = tabledata

    def create(self):
        is_rename, con_mem = self.__require_rename_table()
        src_table_name = con_mem.get_table_name_list()[0]
        dst_table_name = src_table_name

        if is_rename:
            dst_table_name = self.__make_unique_table_name(src_table_name)

            simplesqlite.copy_table(
                src_con=con_mem, dst_con=self.__dst_con,
                src_table_name=src_table_name,
                dst_table_name=dst_table_name)
        else:
            simplesqlite.append_table(
                src_con=con_mem, dst_con=self.__dst_con,
                table_name=dst_table_name)

    def __require_rename_table(self):
        con_mem = simplesqlite.connect_sqlite_db_mem()
        con_mem.create_table_from_tabledata(tabledata=self.__tabledata)

        if not self.__dst_con.has_table(self.__tabledata.table_name):
            return (False, con_mem)

        if self.__dst_con.get_attr_name_list(self.__tabledata.table_name) != self.__tabledata.header_list:
            return (True, con_mem)

        con_schema_extractor = SqliteSchemaExtractor(
            self.__dst_con, verbosity_level=1)
        con_mem_schema_extractor = SqliteSchemaExtractor(
            con_mem, verbosity_level=1)

        if con_schema_extractor.get_database_schema() == con_mem_schema_extractor.get_database_schema():
            return (False, con_mem)

        return (True, con_mem)

    def __make_unique_table_name(self, table_name_base):
        exist_table_name_list = self.__dst_con.get_table_name_list()

        if table_name_base not in exist_table_name_list:
            return table_name_base

        suffix_id = 1
        while True:
            table_name_candidate = u"{:s}_{:d}".format(
                table_name_base, suffix_id)

            if table_name_candidate not in exist_table_name_list:
                return table_name_candidate

            suffix_id += 1


@cmd.command()
@click.argument("files", type=str, nargs=-1)
@click.option(
    "-o", "--output-path", metavar="PATH", default=Default.OUTPUT_FILE,
    help="Output path of the SQLite database file. Defaults to '{:s}'.".format(
        Default.OUTPUT_FILE))
@click.pass_context
def file(ctx, files, output_path):
    """
    Convert tabular data within CSV/Excel/HTML/JSON/LTSV/Markdown/SQLite/TSV
    file(s) to a SQLite database file.
    """

    if typepy.is_empty_sequence(files):
        sys.exit(ExitCode.NO_INPUT)

    con = create_database(ctx, output_path)
    verbosity_level = ctx.obj.get(Context.VERBOSITY_LEVEL)
    schema_extractor = get_schema_extractor(con, verbosity_level)
    result_counter = ResultCounter()
    logger = make_logger("{:s} file".format(
        PROGRAM_NAME), ctx.obj[Context.LOG_LEVEL])

    for file_path in files:
        file_path = path.Path(file_path)

        if not file_path.isfile():
            logger.error(u"file not found: {}".format(file_path))
            result_counter.inc_fail()
            continue

        if file_path == output_path:
            logger.warn(
                u"skip a file which has the same path as the output file ({})".format(
                    file_path))
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
                    TableCreator(
                        dst_con=con, tabledata=sqlite_tabledata).create()
                    result_counter.inc_success()
                except (ValueError, IOError) as e:
                    logger.debug(
                        u"path={}, message={}".format(file_path, e))
                    result_counter.inc_fail()
                    continue

                logger.info(get_success_message(
                    verbosity_level, file_path,
                    schema_extractor.get_table_schema_text(
                        sqlite_tabledata.table_name).strip()))
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
    "-o", "--output-path", metavar="PATH", default=Default.OUTPUT_FILE,
    help="Output path of the SQLite database file. Defaults to '{:s}'.".format(
        Default.OUTPUT_FILE))
@click.option(
    "--encoding", type=str, metavar="ENCODING", default=Default.ENCODING,
    help="HTML page read encoding. Defaults to {:s}.".format(Default.ENCODING))
@click.option(
    "--proxy", type=str, metavar="PROXY",
    help="Specify a proxy in the form [user:passwd@]proxy.server:port.")
@click.pass_context
def url(ctx, url, format_name, output_path, encoding, proxy):
    """
    Scrape tabular data from a URL and convert data to a SQLite database file.
    """

    if typepy.is_empty_sequence(url):
        sys.exit(ExitCode.NO_INPUT)

    con = create_database(ctx, output_path)
    verbosity_level = ctx.obj.get(Context.VERBOSITY_LEVEL)
    schema_extractor = get_schema_extractor(con, verbosity_level)
    result_counter = ResultCounter()
    logger = make_logger("{:s} url".format(
        PROGRAM_NAME), ctx.obj[Context.LOG_LEVEL])

    if typepy.is_null_string(proxy):
        proxy = app_config_manager.load().get(ConfigKey.PROXY_SERVER)

    proxies = {
        "http": proxy,
        "https": proxy,
    }

    try:
        loader = create_url_loader(logger, url, format_name, encoding, proxies)
    except ptr.LoaderNotFoundError as e:
        try:
            loader = create_url_loader(logger, url, "html", encoding, proxies)
        except ptr.LoaderNotFoundError as e:
            logger.error(e)
            sys.exit(ExitCode.FAILED_LOADER_NOT_FOUND)

    try:
        for tabledata in loader.load():
            sqlite_tabledata = ptr.SQLiteTableDataSanitizer(
                tabledata).sanitize()

            try:
                TableCreator(
                    dst_con=con, tabledata=sqlite_tabledata).create()
                result_counter.inc_success()
            except (ValueError) as e:
                logger.debug(
                    u"url={}, message={}".format(url, str(e)))
                result_counter.inc_fail()
                continue

            logger.info(get_success_message(
                verbosity_level, url,
                schema_extractor.get_table_schema_text(
                    sqlite_tabledata.table_name).strip()))
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
    "-o", "--output-path", metavar="PATH", default=Default.OUTPUT_FILE,
    help="Output path of the SQLite database file. Defaults to '{:s}'.".format(
        Default.OUTPUT_FILE))
@click.pass_context
def gs(ctx, credentials, title, output_path):
    """
    Convert a spreadsheet in Google Sheets to a SQLite database file.

    CREDENTIALS: OAuth2 Google credentials file.
    TITLE: Title of the Google Sheets to convert.
    """

    con = create_database(ctx, output_path)
    verbosity_level = ctx.obj.get(Context.VERBOSITY_LEVEL)
    schema_extractor = get_schema_extractor(con, verbosity_level)
    result_counter = ResultCounter()
    logger = make_logger("{:s} gs".format(
        PROGRAM_NAME), ctx.obj[Context.LOG_LEVEL])

    loader = ptr.GoogleSheetsTableLoader()
    loader.source = credentials
    loader.title = title

    # if typepy.is_null_string(loader.source):
    #     loader.source = app_config_manager.load().get(
    #         ConfigKey.GS_CREDENTIALS_FILE_PATH)

    try:
        for tabledata in loader.load():
            sqlite_tabledata = ptr.SQLiteTableDataSanitizer(
                tabledata).sanitize()

            try:
                TableCreator(
                    dst_con=con, tabledata=sqlite_tabledata).create()
                result_counter.inc_success()
            except (ptr.ValidationError, ptr.InvalidDataError):
                result_counter.inc_fail()

            logger.info(get_success_message(
                verbosity_level, "google sheets",
                schema_extractor.get_table_schema_text(tabledata.table_name).strip()))
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


@cmd.command()
@click.pass_context
def configure(ctx):
    """
    Configure the following application settings:

    (1) HTTP/HTTPS proxy server URI (for url sub-command).

    Configurations will be written to '~/.sqlitebiter'.
    You can remove these settings by deleting '~/.sqlitebiter'.
    """

    logger = make_logger(
        "{:s} file".format(PROGRAM_NAME), ctx.obj[Context.LOG_LEVEL])

    logger.debug("{} configuration file existence: {}".format(
        PROGRAM_NAME, app_config_manager.exists))

    try:
        sys.exit(app_config_manager.configure())
    except KeyboardInterrupt:
        click.echo()
        sys.exit(errno.EINTR)


if __name__ == '__main__':
    cmd()
