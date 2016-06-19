#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import sys

import readmemaker


PROJECT_NAME = "sqlitebiter"
OUTPUT_DIR = ".."


def write_examples(maker):
    maker.set_indent_level(0)
    maker.write_chapter("Usage")
    maker.write_line_list([
        ".. image:: docs/gif/usage_example.gif",
    ])

    maker.inc_indent_level()
    maker.write_chapter("For more information")
    maker.write_line_list([
        "More examples are available at ",
        "http://%s.readthedocs.io/en/latest/pages/%s/index.html" % (
            PROJECT_NAME.lower(), maker.examples_dir_name),
    ])


def main():
    maker = readmemaker.ReadmeMaker(PROJECT_NAME, OUTPUT_DIR)
    maker.examples_dir_name = u"usage"

    maker.write_introduction_file("badges.txt")

    maker.inc_indent_level()
    maker.write_chapter("Summary")
    maker.write_introduction_file("summary.txt")
    maker.write_introduction_file("feature.txt")

    write_examples(maker)

    maker.write_file(
        maker.doc_page_root_dir_path.joinpath("installation.rst"))

    maker.set_indent_level(0)
    maker.write_chapter("Documentation")
    maker.write_line_list([
        "http://%s.readthedocs.org/en/latest/" % (PROJECT_NAME.lower()),
    ])

    return 0


if __name__ == '__main__':
    sys.exit(main())
