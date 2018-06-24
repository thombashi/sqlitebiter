# encoding: utf-8

'''
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
'''

from __future__ import absolute_import

from sqliteschema import SqliteSchemaExtractor

from ._const import MAX_VERBOSITY_LEVEL


def get_success_message(verbosity_level, source, dst_table_name):
    message_template = u"convert '{:s}' to '{:s}' table"

    return message_template.format(source, dst_table_name.strip())


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
