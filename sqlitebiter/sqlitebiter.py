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
import path
import pytablereader as ptr
import simplesqlite as sqlite
import typepy

from .__version__ import __version__
from ._config import ConfigKey, app_config_manager
from ._const import IPYNB_FORMAT_NAME_LIST, PROGRAM_NAME
from ._enum import Context, ExitCode
from .subcommand import FileConverter, GoogleSheetsConverter, UrlConverter


CONTEXT_SETTINGS = dict(
    help_option_names=["-h", "--help"],
    obj={},
)
QUIET_LOG_LEVEL = logbook.NOTSET

logbook.StderrHandler(
    level=logbook.DEBUG,
    format_string="[{record.level_name}] {record.channel}: {record.message}"
).push_application()


class Default(object):
    OUTPUT_FILE = "out.sqlite"
    ENCODING = "utf-8"


def create_database(ctx, database_path):
    is_append_table = ctx.obj.get(Context.IS_APPEND_TABLE)

    db_path = path.Path(database_path)
    dir_path = db_path.dirname()
    if typepy.is_not_null_string(dir_path):
        dir_path.makedirs_p()

    if is_append_table:
        return sqlite.SimpleSQLite(db_path, "a")

    return sqlite.SimpleSQLite(db_path, "w")


def make_logger(channel_name, log_level):
    import appconfigpy

    logger = logbook.Logger(channel_name)

    if log_level == QUIET_LOG_LEVEL:
        logger.disable()

    logger.level = log_level
    ptr.set_log_level(log_level)
    sqlite.set_log_level(log_level)
    appconfigpy.set_log_level(log_level)

    return logger


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
    CSV/Excel/HTML/JSON/Jupyter Notebook/LDJSON/LTSV/Markdown/Mediawiki/SQLite/SSV/TSV
    file(s) to a SQLite database file.
    """

    if typepy.is_empty_sequence(files):
        sys.exit(ExitCode.NO_INPUT)

    con = create_database(ctx, output_path)
    logger = make_logger("{:s} file".format(PROGRAM_NAME), ctx.obj[Context.LOG_LEVEL])

    file_converter = FileConverter(
        logger=logger,
        con=con,
        index_list=ctx.obj.get(Context.INDEX_LIST),
        verbosity_level=ctx.obj.get(Context.VERBOSITY_LEVEL),
        format_name=format_name,
        encoding=encoding)

    for file_path in files:
        file_converter.convert(file_path)

    file_converter.write_completion_message()

    sys.exit(file_converter.get_return_code())


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

    if typepy.is_empty_sequence(url):
        sys.exit(ExitCode.NO_INPUT)

    con = create_database(ctx, output_path)
    logger = make_logger("{:s} url".format(PROGRAM_NAME), ctx.obj[Context.LOG_LEVEL])

    if typepy.is_empty_sequence(encoding):
        encoding = app_config_manager.load().get(ConfigKey.DEFAULT_ENCODING)
        logger.debug("use default encoding: {}".format(encoding))

    if typepy.is_null_string(proxy):
        proxy = app_config_manager.load().get(ConfigKey.PROXY_SERVER)

    converter = UrlConverter(
        logger=logger,
        con=con,
        index_list=ctx.obj.get(Context.INDEX_LIST),
        verbosity_level=ctx.obj.get(Context.VERBOSITY_LEVEL),
        format_name=format_name,
        encoding=encoding,
        proxy=proxy)

    converter.convert(url)

    converter.write_completion_message()

    sys.exit(converter.get_return_code())


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
    logger = make_logger("{:s} gs".format(PROGRAM_NAME), ctx.obj[Context.LOG_LEVEL])

    converter = GoogleSheetsConverter(
        logger=logger,
        con=con,
        index_list=ctx.obj.get(Context.INDEX_LIST),
        verbosity_level=ctx.obj.get(Context.VERBOSITY_LEVEL))

    converter.convert(credentials, title)

    converter.write_completion_message()

    sys.exit(converter.get_return_code())


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
