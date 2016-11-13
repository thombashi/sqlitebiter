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

from ._counter import ResultCounter


CONTEXT_SETTINGS = dict(
    help_option_names=["-h", "--help"],
    obj={},
)

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
    "-o", "--output-path", default="out.sqlite",
    help="Output path of the SQLite database file")
@click.pass_context
def file(ctx, files, output_path):
    """
    Convert CSV/Excel/HTML/Markdown/JSON file(s) to a SQLite database file.
    """

    if dataproperty.is_empty_sequence(files):
        return 0

    con = create_database(output_path)
    result_counter = ResultCounter()

    logger = logbook.Logger("sqlitebiter file")
    _setup_logger_from_context(ctx, logger)

    for file_path in files:
        file_path = path.Path(file_path)
        if not file_path.isfile():
            continue

        try:
            loader = ptr.TableFileLoader(file_path)
        except ptr.InvalidFilePathError as e:
            logger.debug(e)
            continue
        except ptr.LoaderNotFoundError:
            logger.debug(
                "loader not found that coincide with '{}'".format(file_path))
            continue

        try:
            for tabledata in loader.load():
                try:
                    con.create_table_from_tabledata(
                        ptr.SQLiteTableDataSanitizer(tabledata).sanitize())
                    result_counter.inc_success()
                except (ValueError, IOError) as e:
                    logger.debug(
                        "path={:s}, message={:s}".format(file_path, e))
                    result_counter.inc_fail()
                    continue

                click.echo("convert '{:s}' to '{:s}' table".format(
                    file_path, tabledata.table_name))
        except ptr.OpenError as e:
            logger.error("open error: file={:s}, message='{:s}'".format(
                file_path, str(e)))
        except ptr.ValidationError as e:
            logger.error(
                "invalid {:s} data format: path={:s}, message={:s}".format(
                    _get_format_type_from_path(file_path), file_path, str(e)))
            result_counter.inc_fail()
        except ptr.InvalidDataError as e:
            logger.error(
                "invalid {:s} data: path={:s}, message={:s}".format(
                    _get_format_type_from_path(file_path), file_path, str(e)))
            result_counter.inc_fail()

    sys.exit(result_counter.get_return_code())


@cmd.command()
@click.argument(
    "credentials", type=click.Path(exists=True))
@click.argument(
    "title", type=str)
@click.option(
    "-o", "--output-path", default="out.sqlite",
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
    except AttributeError:
        logger.error("invalid credentials data: path={:s}".format(credentials))
    except (ptr.ValidationError, ptr.InvalidDataError) as e:
        logger.error(
            "invalid credentials data: path={:s}, message={:s}".format(
                credentials, str(e)))
        result_counter.inc_fail()

    sys.exit(result_counter.get_return_code())


if __name__ == '__main__':
    cmd()
