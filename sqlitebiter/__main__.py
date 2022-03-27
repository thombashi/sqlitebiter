"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import os
import sys
from textwrap import dedent
from typing import Dict, Tuple

import appconfigpy
import click
import msgfy
import path
import pytablereader as ptr
import simplesqlite as sqlite
import typepy
from loguru import logger

from .__version__ import __version__
from ._common import DEFAULT_DUP_COL_HANDLER
from ._config import ConfigKey, app_config_mgr
from ._const import IPYNB_FORMAT_NAME_LIST, PROGRAM_NAME, ExitCode
from ._enum import Context, DupDatabase
from .converter import FileConverter, GoogleSheetsConverter, TextConverter, UrlConverter


try:
    import ujson as json
except ImportError:
    import json  # type: ignore


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], obj={})
QUIET_LOG_LEVEL = "QUIET"
COMMAND_EPILOG = dedent(
    """\
    Documentation: https://sqlitebiter.rtfd.io/
    Issue tracker: https://github.com/thombashi/sqlitebiter/issues
    """
)


class Default:
    OUTPUT_FILE = "out.sqlite"
    ENCODING = "utf-8"


def create_database(
    database_path: str, dup_table: DupDatabase, max_workers: int
) -> Tuple[sqlite.SimpleSQLite, bool]:
    db_path = path.Path(database_path)
    dir_path = db_path.dirname()

    if typepy.is_not_null_string(dir_path):
        dir_path.makedirs_p()

    is_create_db = not db_path.isfile()

    if dup_table == DupDatabase.APPEND:
        return (sqlite.SimpleSQLite(db_path, "a", max_workers=max_workers), is_create_db)

    return (sqlite.SimpleSQLite(db_path, "w", max_workers=max_workers), is_create_db)


def initialize_logger(name: str, log_level: str) -> None:
    logger.remove()

    if log_level == QUIET_LOG_LEVEL:
        logger.disable(name)
        return

    if log_level == "DEBUG":
        log_format = (
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )
    else:
        log_format = "<level>[{level}]</level> {message}"

    logger.add(sys.stderr, colorize=True, format=log_format, level=log_level)
    logger.enable(name)
    ptr.set_logger(True)
    sqlite.set_logger(True)
    appconfigpy.set_logger(True)


def finalize(con, converter, is_create_db: bool) -> int:
    converter.write_completion_message()
    database_path = con.database_path
    con.close()

    if all([os.path.isfile(database_path), converter.get_success_count() == 0, is_create_db]):
        os.remove(database_path)

    return converter.get_return_code()


def load_convert_config(logger, config_filepath: str, subcommand: str) -> Dict:
    if not config_filepath:
        return {}

    if not os.path.isfile(config_filepath):
        logger.debug(f"{config_filepath} not found")
        return {}

    with open(config_filepath, encoding="utf-8") as f:
        configs = json.load(f)

    return configs.get(subcommand)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__, message="%(prog)s %(version)s")
@click.option(
    "-o",
    "--output-path",
    metavar="PATH",
    default=Default.OUTPUT_FILE,
    help=f"""
        Output path of the SQLite database file.
        Defaults to '{Default.OUTPUT_FILE:s}'.
    """,
)
@click.option(
    "-a", "--append", "is_append_table", is_flag=True, help="Append table(s) to existing database."
)
@click.option(
    "--add-primary-key",
    "add_pri_key_name",
    metavar="PRIMARY_KEY_NAME",
    help="Add 'PRIMARY KEY AUTOINCREMENT' column to a converted table with the specified name.",
)
@click.option(
    "--convert-config",
    help=dedent(
        """\
        [experimental]
        Configurations for data conversion. The option can be used only for url subcommand.
        """
    ),
)
@click.option(
    "-i",
    "--index",
    "index_list",
    metavar="INDEX_ATTR",
    default="",
    help="Comma separated attribute names to create indices.",
)
@click.option(
    "--no-type-inference",
    is_flag=True,
    help="All of the columns assume as TEXT data type in creating tables.",
)
@click.option(
    "--type-hint-header",
    "is_type_hint_header",
    is_flag=True,
    help=dedent(
        """\
        Use headers suffix as type hints.
        If there are type hints, converting columns by datatype corresponding with type hints.
        The following suffixes can be recognized as type hints (case insensitive):
        "text": TEXT datatype.
        "integer": INTEGER datatype.
        "real": REAL datatype.
        """
    ),
)
@click.option("--replace-symbol", "symbol_replace_value", help="Replace symbols in attributes.")
@click.option("-v", "--verbose", "verbosity_level", count=True)
@click.option(
    "--max-workers",
    metavar="WORKERS",
    type=int,
    default=1,
    help=dedent(
        """\
        Specify maximum number of workers that the command may use.
        defaults to 1.
        """
    ),
)
@click.option("--debug", "log_level", flag_value="DEBUG", help="For debug print.")
@click.option(
    "-q",
    "--quiet",
    "log_level",
    flag_value=QUIET_LOG_LEVEL,
    help="Suppress execution log messages.",
)
@click.pass_context
def cmd(
    ctx,
    output_path,
    is_append_table,
    add_pri_key_name,
    convert_config,
    index_list,
    no_type_inference,
    is_type_hint_header,
    symbol_replace_value,
    verbosity_level,
    max_workers,
    log_level,
):
    ctx.obj[Context.OUTPUT_PATH] = output_path
    ctx.obj[Context.SYMBOL_REPLACE_VALUE] = symbol_replace_value
    ctx.obj[Context.DUP_DATABASE] = DupDatabase.APPEND if is_append_table else DupDatabase.OVERWRITE
    ctx.obj[Context.ADD_PRIMARY_KEY_NAME] = add_pri_key_name
    ctx.obj[Context.INDEX_LIST] = index_list.split(",")
    ctx.obj[Context.CONVERT_CONFIG] = convert_config
    ctx.obj[Context.TYPE_INFERENCE] = not no_type_inference
    ctx.obj[Context.TYPE_HINT_HEADER] = is_type_hint_header
    ctx.obj[Context.VERBOSITY_LEVEL] = verbosity_level
    ctx.obj[Context.MAX_WORKERS] = max_workers
    ctx.obj[Context.LOG_LEVEL] = "INFO" if log_level is None else log_level

    sqlite.SimpleSQLite.dup_col_handler = DEFAULT_DUP_COL_HANDLER


@cmd.command(epilog=COMMAND_EPILOG)
@click.pass_context
def version(ctx):
    """
    Show version information
    """

    import envinfopy

    click.echo(
        envinfopy.dumps(
            ["SimpleSQLite", "pytablereader"],
            format="itemize",
            additional_envinfo={"sqlitebiter": __version__},
            verbosity_level=ctx.obj[Context.VERBOSITY_LEVEL],
        )
    )


@cmd.command(epilog=COMMAND_EPILOG)
@click.argument("files", type=str, nargs=-1)
@click.option(
    "-r", "--recursive", is_flag=True, help="Read all files under each directory, recursively."
)
@click.option("--pattern", metavar="PATTERN", help="Convert files matching PATTERN.")
@click.option("--exclude", metavar="PATTERN", help="Exclude files matching PATTERN.")
@click.option("--follow-symlinks", is_flag=True, help="Follow symlinks.")
@click.option(
    "-f",
    "--format",
    "format_name",
    type=click.Choice(ptr.TableFileLoader.get_format_names() + IPYNB_FORMAT_NAME_LIST),
    help="Data format to loading (auto-detect from file extensions in default).",
)
@click.option(
    "--encoding",
    metavar="ENCODING",
    help="Encoding to load files. Auto-detection from files in default.",
)
@click.pass_context
def file(ctx, files, recursive, pattern, exclude, follow_symlinks, format_name, encoding):
    """
    Convert tabular data within
    CSV/Excel/HTML/JSON/Jupyter Notebook/LDJSON/LTSV/Markdown/Mediawiki/SQLite/SSV/TSV
    file(s) or named pipes to a SQLite database file.
    """

    initialize_logger(f"{PROGRAM_NAME:s} file", ctx.obj[Context.LOG_LEVEL])

    if typepy.is_empty_sequence(files):
        logger.error(f"require at least one file specification.\n\n{ctx.get_help()}")
        sys.exit(ExitCode.NO_INPUT)

    convert_configs = load_convert_config(
        logger, ctx.obj[Context.CONVERT_CONFIG], subcommand="file"
    )

    max_workers = ctx.obj.get(Context.MAX_WORKERS)
    con, is_create_db = create_database(
        ctx.obj[Context.OUTPUT_PATH], ctx.obj[Context.DUP_DATABASE], max_workers=max_workers
    )
    converter = FileConverter(
        logger=logger,
        con=con,
        symbol_replace_value=ctx.obj[Context.SYMBOL_REPLACE_VALUE],
        add_pri_key_name=ctx.obj[Context.ADD_PRIMARY_KEY_NAME],
        convert_configs=convert_configs,
        index_list=ctx.obj.get(Context.INDEX_LIST),
        is_type_inference=ctx.obj[Context.TYPE_INFERENCE],
        is_type_hint_header=ctx.obj[Context.TYPE_HINT_HEADER],
        verbosity_level=ctx.obj.get(Context.VERBOSITY_LEVEL),
        max_workers=max_workers,
        format_name=format_name,
        encoding=encoding,
        exclude_pattern=exclude,
        follow_symlinks=follow_symlinks,
    )

    for file_path in files:
        dir_path_obj = path.Path(file_path)

        if not follow_symlinks and dir_path_obj.islink() and dir_path_obj.isdir():
            logger.debug(
                "skip symlink to a directory: {} -> {}".format(
                    dir_path_obj, dir_path_obj.readlink()
                )
            )
            continue

        if recursive and dir_path_obj.isdir():
            for file_path_obj in dir_path_obj.walkfiles(pattern):
                converter.convert(file_path_obj)
        else:
            converter.convert(file_path)

    sys.exit(finalize(con, converter, is_create_db))


@cmd.command(epilog=COMMAND_EPILOG)
@click.argument(
    "format_name",
    type=click.Choice(ptr.TableTextLoader.get_format_names() + IPYNB_FORMAT_NAME_LIST),
)
@click.pass_context
def stdin(ctx, format_name):
    """
    Convert tabular data within
    CSV/HTML/JSON/Jupyter Notebook/LDJSON/LTSV/Markdown/Mediawiki/SSV/TSV
    text to a SQLite database file.
    """

    initialize_logger(f"{PROGRAM_NAME:s} stdin", ctx.obj[Context.LOG_LEVEL])

    convert_configs = load_convert_config(
        logger, ctx.obj[Context.CONVERT_CONFIG], subcommand="stdin"
    )

    max_workers = ctx.obj.get(Context.MAX_WORKERS)
    con, is_create_db = create_database(
        ctx.obj[Context.OUTPUT_PATH], ctx.obj[Context.DUP_DATABASE], max_workers=max_workers
    )
    converter = TextConverter(
        logger=logger,
        con=con,
        symbol_replace_value=ctx.obj[Context.SYMBOL_REPLACE_VALUE],
        add_pri_key_name=ctx.obj[Context.ADD_PRIMARY_KEY_NAME],
        convert_configs=convert_configs,
        index_list=ctx.obj.get(Context.INDEX_LIST),
        is_type_inference=ctx.obj[Context.TYPE_INFERENCE],
        is_type_hint_header=ctx.obj[Context.TYPE_HINT_HEADER],
        verbosity_level=ctx.obj.get(Context.VERBOSITY_LEVEL),
        max_workers=max_workers,
        format_name=format_name,
    )

    converter.convert(sys.stdin.read())

    sys.exit(finalize(con, converter, is_create_db))


@cmd.command(epilog=COMMAND_EPILOG)
@click.argument("url", type=str)
@click.option(
    "-f",
    "--format",
    "format_name",
    type=click.Choice(ptr.TableUrlLoader.get_format_names() + IPYNB_FORMAT_NAME_LIST),
    help="Data format to loading (defaults to html).",
)
@click.option(
    "-e",
    "--encoding",
    type=str,
    metavar="ENCODING",
    help=f"HTML page read encoding. Defaults to {Default.ENCODING:s}.",
)
@click.option(
    "-p",
    "--proxy",
    type=str,
    metavar="PROXY",
    help="Specify a proxy in the form [user:passwd@]proxy.server:port.",
)
@click.pass_context
def url(ctx, url, format_name, encoding, proxy):
    """
    Scrape tabular data from a URL and convert data to a SQLite database file.
    """

    if typepy.is_empty_sequence(url):
        sys.exit(ExitCode.NO_INPUT)

    initialize_logger(f"{PROGRAM_NAME:s} url", ctx.obj[Context.LOG_LEVEL])

    try:
        app_configs = app_config_mgr.load()
    except ValueError as e:
        logger.debug(msgfy.to_debug_message(e))
        app_configs = {}

    if typepy.is_empty_sequence(encoding):
        encoding = app_configs.get(ConfigKey.DEFAULT_ENCODING)
        logger.debug(f"use default encoding: {encoding}")

    if typepy.is_null_string(proxy):
        proxy = app_configs.get(ConfigKey.PROXY_SERVER)

    convert_configs = load_convert_config(logger, ctx.obj[Context.CONVERT_CONFIG], subcommand="url")

    max_workers = ctx.obj.get(Context.MAX_WORKERS)
    con, is_create_db = create_database(
        ctx.obj[Context.OUTPUT_PATH], ctx.obj[Context.DUP_DATABASE], max_workers=max_workers
    )
    converter = UrlConverter(
        logger=logger,
        con=con,
        symbol_replace_value=ctx.obj[Context.SYMBOL_REPLACE_VALUE],
        add_pri_key_name=ctx.obj[Context.ADD_PRIMARY_KEY_NAME],
        convert_configs=convert_configs,
        index_list=ctx.obj.get(Context.INDEX_LIST),
        is_type_inference=ctx.obj[Context.TYPE_INFERENCE],
        is_type_hint_header=ctx.obj[Context.TYPE_HINT_HEADER],
        verbosity_level=ctx.obj.get(Context.VERBOSITY_LEVEL),
        max_workers=max_workers,
        format_name=format_name,
        encoding=encoding,
        proxy=proxy,
    )

    converter.convert(url)

    sys.exit(finalize(con, converter, is_create_db))


@cmd.command(epilog=COMMAND_EPILOG)
@click.argument("credentials", type=click.Path(exists=True))
@click.argument("title", type=str)
@click.pass_context
def gs(ctx, credentials, title):
    """
    Convert a spreadsheet in Google Sheets to a SQLite database file.

    CREDENTIALS: OAuth2 Google credentials file.
    TITLE: Title of the Google Sheets to convert.
    """

    initialize_logger(f"{PROGRAM_NAME:s} gs", ctx.obj[Context.LOG_LEVEL])

    max_workers = ctx.obj.get(Context.MAX_WORKERS)
    con, is_create_db = create_database(
        ctx.obj[Context.OUTPUT_PATH], ctx.obj[Context.DUP_DATABASE], max_workers=max_workers
    )
    convert_configs = load_convert_config(
        logger, ctx.obj[Context.CONVERT_CONFIG], subcommand="file"
    )

    converter = GoogleSheetsConverter(
        logger=logger,
        con=con,
        symbol_replace_value=ctx.obj[Context.SYMBOL_REPLACE_VALUE],
        add_pri_key_name=ctx.obj[Context.ADD_PRIMARY_KEY_NAME],
        convert_configs=convert_configs,
        index_list=ctx.obj.get(Context.INDEX_LIST),
        is_type_inference=ctx.obj[Context.TYPE_INFERENCE],
        is_type_hint_header=ctx.obj[Context.TYPE_HINT_HEADER],
        verbosity_level=ctx.obj.get(Context.VERBOSITY_LEVEL),
        max_workers=max_workers,
    )

    converter.convert(credentials, title)

    sys.exit(finalize(con, converter, is_create_db))


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

    initialize_logger(f"{PROGRAM_NAME:s} configure", ctx.obj[Context.LOG_LEVEL])

    logger.debug(f"{PROGRAM_NAME} configuration file existence: {app_config_mgr.exists}")

    sys.exit(app_config_mgr.configure())


@cmd.command(epilog=COMMAND_EPILOG)
@click.argument("shell", type=click.Choice(["bash", "zsh"]))
@click.pass_context
def completion(ctx, shell):
    """
    A helper command to setup command completion.

    To setup for bash:

        sqlitebiter completion bash >> ~/.bashrc

    To setup for zsh:

        sqlitebiter completion zsh >> ~/.zshrc
    """

    if shell == "bash":
        click.echo(
            dedent(
                """\
            _sqlitebiter_completion() {
                local IFS=$'
            '
                COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                            COMP_CWORD=$COMP_CWORD \
                            _SQLITEBITER_COMPLETE=complete $1 ) )
                return 0
            }

            _sqlitebiter_completionetup() {
                local COMPLETION_OPTIONS=""
                local BASH_VERSION_ARR=(${BASH_VERSION//./ })
                # Only BASH version 4.4 and later have the nosort option.
                if [ ${BASH_VERSION_ARR[0]} -gt 4 ] || ([ ${BASH_VERSION_ARR[0]} -eq 4 ] && [ ${BASH_VERSION_ARR[1]} -ge 4 ]); then
                    COMPLETION_OPTIONS="-o nosort"
                fi

                complete $COMPLETION_OPTIONS -F _sqlitebiter_completion sqlitebiter
            }
            """
            )
        )
    elif shell == "zsh":
        click.echo(
            dedent(
                """\
                _sqlitebiter_completion() {
                    local -a completions
                    local -a completions_with_descriptions
                    local -a response
                    response=("${(@f)$( env COMP_WORDS="${words[*]}" \
                                        COMP_CWORD=$((CURRENT-1)) \
                                        _SQLITEBITER_COMPLETE="complete_zsh" \
                                        sqlitebiter )}")

                    for key descr in ${(kv)response}; do
                    if [[ "$descr" == "_" ]]; then
                        completions+=("$key")
                    else
                        completions_with_descriptions+=("$key":"$descr")
                    fi
                    done

                    if [ -n "$completions_with_descriptions" ]; then
                        _describe -V unsorted completions_with_descriptions -U -Q
                    fi

                    if [ -n "$completions" ]; then
                        compadd -U -V unsorted -Q -a completions
                    fi
                    compstate[insert]="automenu"
                }

                compdef _sqlitebiter_completion sqlitebiter;
                """
            )
        )
