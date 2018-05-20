# encoding: utf-8

'''
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
'''

from __future__ import absolute_import


def get_success_message(verbosity_level, source, to_table_name):
    message_template = u"convert '{:s}' to '{:s}' table"

    return message_template.format(source, to_table_name.strip())
