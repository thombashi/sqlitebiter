# encoding: utf-8

'''
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
'''

from __future__ import absolute_import, unicode_literals


def get_success_message(source, schema_extractor, table_name, verbosity_level):
    table_schema = schema_extractor.fetch_table_schema(table_name.strip())

    return "convert '{source:s}' to '{table_info:s}' table".format(
        source=source,
        table_info=table_schema.dumps(output_format="text", verbosity_level=verbosity_level))
