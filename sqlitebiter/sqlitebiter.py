#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

import errno
import sys

import click
import logbook
import msgfy
import path
import pytablereader as ptr
import simplesqlite
import six
import typepy
from simplesqlite import SQLiteTableDataSanitizer
from sqliteschema import SqliteSchemaExtractor

from .__version__ import __version__
from ._common import get_success_message
from ._config import ConfigKey, app_config_manager
from ._const import IPYNB_FORMAT_NAME_LIST, PROGRAM_NAME
from ._counter import ResultCounter
from ._dict_converter import DictConverter
from ._enum import Context, ExitCode
from ._table_creator import TableCreator


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


table_not_found_msg_format = "table not found in {}"


class Default(object):
    OUTPUT_FILE = "out.sqlite"
    ENCODING = "utf-8"


def get_schema_extractor(source, verbosity_level):
    found_ptw = True
    try:
        import pytablewriter  # noqa: W0611
    except ImportError:
        found_ptw = False

    if verbosity_level >= MAX_VERBOSITY_LEVEL and found_ptw:
        return SqliteSchemaExtractor(source, verbosity_level=0, output_format="table")

    if verbosity_level >= 1:
        return SqliteSchemaExtractor(source, verbosity_level=3, output_format="text")

    if verbosity_level == 0:
        return SqliteSchemaExtractor(source, verbosity_level=0, output_format="text")

    raise ValueError("invalid verbosity_level: {}".format(verbosity_level))


def create_database(ctx, database_path):
    is_append_table = ctx.obj.get(Context.IS_APPEND_TABLE)

    db_path = path.Path(database_path)
    dir_path = db_path.dirname()
    if typepy.is_not_null_string(dir_path):
        dir_path.makedirs_p()

    if is_append_table:
        return simplesqlite.SimpleSQLite(db_path, "a")

    return simplesqlite.SimpleSQLite(db_path, "w")


def write_completion_message(logger, database_path, result_counter):
    database_path_msg = u"database path: {:s}".format(database_path)

    logger.debug(u"----- {:s} completed -----".format(PROGRAM_NAME))
    logger.info(u"number of created tables: {:d}".format(result_counter.success_count))
    if result_counter.success_count > 0:
        logger.info(database_path_msg)
        logger.debug(u"----- database schema -----")
        logger.debug(get_schema_extractor(database_path, MAX_VERBOSITY_LEVEL).dumps())
    else:
        logger.debug(database_path_msg)


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


def create_url_loader(logger, source_url, format_name, encoding, proxies):
    try:
        return ptr.TableUrlLoader(source_url, format_name, encoding=encoding, proxies=proxies)
    except ptr.HTTPError as e:
        logger.error(msgfy.to_error_message(e))
        sys.exit(ExitCode.FAILED_HTTP)
    except ptr.ProxyError as e:
        logger.error(msgfy.to_error_message(e))
        sys.exit(errno.ECONNABORTED)


def _get_format_type_from_path(file_path):
    return file_path.ext.lstrip(".")


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
@click.option(
    "-a", "--append", "is_append_table", is_flag=True,
    help="append table(s) to existing database.")
@click.option(
    "-i", "--index", "index_list", default="",
    help="comma separated attribute names to create indices.")
@click.option("-v", "--verbose", "verbosity_level", count=True)
@click.option(
    "--debug", "log_level", flag_value=logbook.DEBUG,
    help="for debug print.")
@click.option(
    "--quiet", "log_level", flag_value=QUIET_LOG_LEVEL,
    help="suppress execution log messages.")
@click.pass_context
def cmd(ctx, is_append_table, index_list, verbosity_level, log_level):
    ctx.obj[Context.IS_APPEND_TABLE] = is_append_table
    ctx.obj[Context.INDEX_LIST] = index_list.split(",")
    ctx.obj[Context.VERBOSITY_LEVEL] = verbosity_level
    ctx.obj[Context.LOG_LEVEL] = (logbook.INFO if log_level is None else log_level)


@cmd.command()
@click.argument("files", type=str, nargs=-1)
@click.option(
    "-f", "--format", "format_name",
    type=click.Choice(ptr.TableFileLoader.get_format_name_list() + IPYNB_FORMAT_NAME_LIST),
    help="Data format to loading (auto-detect from file extensions in default).")
@click.option(
    "-o", "--output-path", metavar="PATH", default=Default.OUTPUT_FILE,
    help="Output path of the SQLite database file. Defaults to '{:s}'.".format(
        Default.OUTPUT_FILE))
@click.option(
    "--encoding", metavar="ENCODING",
    help="Encoding to load files. Auto-detection from files in default.")
@click.pass_context
def file(ctx, files, format_name, output_path, encoding):
    """
    Convert tabular data within
    CSV/Excel/HTML/JSON/Jupyter Notebook/LTSV/Markdown/Mediawiki/SQLite/SSV/TSV
    file(s) to a SQLite database file.
    """

    from ._ipynb_converter import is_ipynb_file_path, load_ipynb_file, convert_nb

    if typepy.is_empty_sequence(files):
        sys.exit(ExitCode.NO_INPUT)

    con = create_database(ctx, output_path)
    verbosity_level = ctx.obj.get(Context.VERBOSITY_LEVEL)
    schema_extractor = get_schema_extractor(con, verbosity_level)
    result_counter = ResultCounter()
    logger = make_logger("{:s} file".format(PROGRAM_NAME), ctx.obj[Context.LOG_LEVEL])
    table_creator = TableCreator(logger=logger, dst_con=con)

    for file_path in files:
        file_path = path.Path(file_path)

        if not file_path.isfile():
            logger.error(u"file not found: {}".format(file_path))
            result_counter.inc_fail()
            continue

        if file_path == output_path:
            logger.warn(
                u"skip a file which has the same path as the output file ({})".format(file_path))
            continue

        logger.debug(u"converting '{}'".format(file_path))
        convert_count = result_counter.total_count

        if format_name in IPYNB_FORMAT_NAME_LIST or is_ipynb_file_path(file_path):
            convert_nb(
                logger,
                con,
                result_counter,
                nb=load_ipynb_file(file_path, encoding=encoding))
            for table_name in con.get_table_name_list():
                logger.info(get_success_message(
                    verbosity_level, file_path,
                    schema_extractor.get_table_schema_text(table_name)))
                result_counter.inc_success()
            if result_counter.total_count == convert_count:
                table_not_found_msg_format.format(file_path)
            continue

        try:
            loader = ptr.TableFileLoader(file_path, format_name=format_name, encoding=encoding)
        except ptr.InvalidFilePathError as e:
            logger.debug(msgfy.to_debug_message(e))
            result_counter.inc_fail()
            continue
        except ptr.LoaderNotFoundError:
            logger.debug(u"loader not found that coincide with '{}'".format(file_path))
            result_counter.inc_fail()
            continue

        try:
            for table_data in loader.load():
                logger.debug(u"loaded tabledata: {}".format(six.text_type(table_data)))

                sqlite_tabledata = SQLiteTableDataSanitizer(table_data).normalize()

                try:
                    table_creator.create(sqlite_tabledata, ctx.obj.get(Context.INDEX_LIST))
                    result_counter.inc_success()
                except (ValueError, IOError) as e:
                    logger.debug(u"exception={:s}, path={}, message={}".format(
                        type(e).__name__, file_path, e))
                    result_counter.inc_fail()
                    continue

                logger.info(get_success_message(
                    verbosity_level, file_path,
                    schema_extractor.get_table_schema_text(sqlite_tabledata.table_name)))
        except ptr.OpenError as e:
            logger.error(u"{:s}: open error: file={}, message='{}'".format(
                e.__class__.__name__, file_path, str(e)))
            result_counter.inc_fail()
        except ptr.ValidationError as e:
            if loader.format_name == "json":
                dict_converter = DictConverter(
                    logger, table_creator, result_counter, schema_extractor, verbosity_level,
                    source=file_path, index_list=ctx.obj.get(Context.INDEX_LIST))

                try:
                    dict_converter.to_sqlite_table(loader.loader.load_dict(), [])
                except AttributeError:
                    pass
                else:
                    continue

            logger.error(u"{:s}: invalid {} data format: path={}, message={}".format(
                e.__class__.__name__, _get_format_type_from_path(file_path), file_path, str(e)))
            result_counter.inc_fail()
        except ptr.DataError as e:
            logger.error(u"{:s}: invalid {} data: path={}, message={}".format(
                e.__class__.__name__, _get_format_type_from_path(file_path), file_path, str(e)))
            result_counter.inc_fail()

        if result_counter.total_count == convert_count:
            logger.warn(table_not_found_msg_format.format(file_path))

    write_completion_message(logger, output_path, result_counter)

    sys.exit(result_counter.get_return_code())


def get_logging_url_path(url):
    from six.moves.urllib.parse import urlparse

    result = urlparse(url)

    return result.netloc + result.path


@cmd.command()
@click.argument("url", type=str)
@click.option(
    "-f", "--format", "format_name",
    type=click.Choice(ptr.TableUrlLoader.get_format_name_list() + IPYNB_FORMAT_NAME_LIST),
    help="Data format to loading (defaults to html).")
@click.option(
    "-o", "--output-path", metavar="PATH", default=Default.OUTPUT_FILE,
    help="Output path of the SQLite database file. Defaults to '{:s}'.".format(
        Default.OUTPUT_FILE))
@click.option(
    "-e", "--encoding", type=str, metavar="ENCODING",
    help="HTML page read encoding. Defaults to {:s}.".format(Default.ENCODING))
@click.option(
    "-p", "--proxy", type=str, metavar="PROXY",
    help="Specify a proxy in the form [user:passwd@]proxy.server:port.")
@click.pass_context
def url(ctx, url, format_name, output_path, encoding, proxy):
    """
    Scrape tabular data from a URL and convert data to a SQLite database file.
    """

    from ._ipynb_converter import is_ipynb_url, load_ipynb_url, convert_nb

    if typepy.is_empty_sequence(url):
        sys.exit(ExitCode.NO_INPUT)

    con = create_database(ctx, output_path)
    verbosity_level = ctx.obj.get(Context.VERBOSITY_LEVEL)
    schema_extractor = get_schema_extractor(con, verbosity_level)
    result_counter = ResultCounter()
    logger = make_logger("{:s} url".format(PROGRAM_NAME), ctx.obj[Context.LOG_LEVEL])

    if typepy.is_empty_sequence(encoding):
        encoding = app_config_manager.load().get(ConfigKey.DEFAULT_ENCODING)
        logger.debug("use default encoding: {}".format(encoding))

    if typepy.is_null_string(proxy):
        proxy = app_config_manager.load().get(ConfigKey.PROXY_SERVER)

    proxies = {
        "http": proxy,
        "https": proxy,
    }

    if format_name in IPYNB_FORMAT_NAME_LIST or is_ipynb_url(url):
        convert_nb(logger, con, result_counter, nb=load_ipynb_url(url, proxies=proxies))
        for table_name in con.get_table_name_list():
            logger.info(get_success_message(
                verbosity_level, get_logging_url_path(url),
                schema_extractor.get_table_schema_text(table_name)))
            result_counter.inc_success()
        if result_counter.total_count == 0:
            table_not_found_msg_format.format(url)
        else:
            write_completion_message(logger, output_path, result_counter)

        sys.exit(result_counter.get_return_code())

    try:
        loader = create_url_loader(logger, url, format_name, encoding, proxies)
    except ptr.LoaderNotFoundError as e:
        logger.debug(e)

        try:
            loader = create_url_loader(logger, url, "html", encoding, proxies)
        except ptr.LoaderNotFoundError as e:
            logger.error(msgfy.to_error_message(e))
            sys.exit(ExitCode.FAILED_LOADER_NOT_FOUND)

    table_creator = TableCreator(logger=logger, dst_con=con)

    try:
        for table_data in loader.load():
            logger.debug(u"loaded table_data: {}".format(six.text_type(table_data)))

            sqlite_tabledata = SQLiteTableDataSanitizer(table_data).normalize()

            try:
                table_creator.create(sqlite_tabledata, ctx.obj.get(Context.INDEX_LIST))
                result_counter.inc_success()
            except simplesqlite.OperationalError as e:
                logger.error(u"{:s}: failed to convert: url={}, message={}".format(
                    e.__class__.__name__, url, e.message))
                result_counter.inc_fail()
                continue
            except ValueError as e:
                logger.debug(u"{:s}: url={}, message={}".format(e.__class__.__name__, url, str(e)))
                result_counter.inc_fail()
                continue

            logger.info(get_success_message(
                verbosity_level, get_logging_url_path(url),
                schema_extractor.get_table_schema_text(sqlite_tabledata.table_name)))
    except ptr.ValidationError as e:
        is_fail = True
        if loader.format_name == "json":
            dict_converter = DictConverter(
                logger, table_creator, result_counter, schema_extractor, verbosity_level,
                source=url, index_list=ctx.obj.get(Context.INDEX_LIST))

            try:
                dict_converter.to_sqlite_table(loader.loader.load_dict(), [])
            except AttributeError:
                pass
            else:
                is_fail = False

        if is_fail:
            logger.error(u"{:s}: url={}, message={}".format(e.__class__.__name__, url, str(e)))
            result_counter.inc_fail()
    except ptr.DataError as e:
        logger.error(u"{:s}: invalid data: url={}, message={}".format(
            e.__class__.__name__, url, str(e)))
        result_counter.inc_fail()

    if result_counter.total_count == 0:
        logger.warn(table_not_found_msg_format.format(url))

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
    logger = make_logger("{:s} gs".format(PROGRAM_NAME), ctx.obj[Context.LOG_LEVEL])
    table_creator = TableCreator(logger=logger, dst_con=con)

    loader = ptr.GoogleSheetsTableLoader()
    loader.source = credentials
    loader.title = title

    # if typepy.is_null_string(loader.source):
    #     loader.source = app_config_manager.load().get(
    #         ConfigKey.GS_CREDENTIALS_FILE_PATH)

    try:
        for table_data in loader.load():
            logger.debug(u"loaded table_data: {}".format(six.text_type(table_data)))

            sqlite_tabledata = SQLiteTableDataSanitizer(table_data).normalize()

            try:
                table_creator.create(sqlite_tabledata, ctx.obj.get(Context.INDEX_LIST))
                result_counter.inc_success()
            except (ptr.ValidationError, ptr.DataError):
                result_counter.inc_fail()

            logger.info(get_success_message(
                verbosity_level, "google sheets",
                schema_extractor.get_table_schema_text(sqlite_tabledata.table_name)))
    except ptr.OpenError as e:
        logger.error(msgfy.to_error_message(e))
        result_counter.inc_fail()
    except (ptr.ValidationError, ptr.DataError) as e:
        logger.error(u"invalid credentials data: path={}, message={}".format(
            credentials, str(e)))
        result_counter.inc_fail()

    write_completion_message(logger, output_path, result_counter)

    sys.exit(result_counter.get_return_code())


@cmd.command()
@click.pass_context
def configure(ctx):
    """
    Configure the following application settings:

    (1) Default encoding to load files.
    (2) HTTP/HTTPS proxy server URI (for url sub-command).

    Configurations are written to '~/.sqlitebiter'.
    You can remove these settings by deleting '~/.sqlitebiter'.
    """

    logger = make_logger("{:s} file".format(PROGRAM_NAME), ctx.obj[Context.LOG_LEVEL])

    logger.debug("{} configuration file existence: {}".format(
        PROGRAM_NAME, app_config_manager.exists))

    try:
        sys.exit(app_config_manager.configure())
    except KeyboardInterrupt:
        click.echo()
        sys.exit(errno.EINTR)


if __name__ == '__main__':
    cmd()
