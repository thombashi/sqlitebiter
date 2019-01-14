#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import sys

from path import Path
from readmemaker import ReadmeMaker


PROJECT_NAME = "sqlitebiter"
OUTPUT_DIR = ".."


def write_examples(maker):
    maker.set_indent_level(0)
    maker.write_chapter("Usage")

    usage_root = Path("pages").joinpath("usage")

    maker.inc_indent_level()
    maker.write_chapter("Create SQLite database from files")

    maker.write_lines(
        [
            ".. image:: https://cdn.rawgit.com/thombashi/sqlitebiter/master/docs/svg/usage_example.svg"
        ]
    )

    maker.write_chapter("Create SQLite database from URL")
    maker.write_file(usage_root.joinpath("url", "usage.txt"))

    maker.inc_indent_level()
    maker.write_chapter("For more information")
    maker.write_lines(
        [
            "More examples are available at ",
            "https://{:s}.rtfd.io/en/latest/pages/{:s}/index.html".format(
                PROJECT_NAME.lower(), maker.examples_dir_name
            ),
        ]
    )


def main():
    maker = ReadmeMaker(
        PROJECT_NAME,
        OUTPUT_DIR,
        is_make_toc=True,
        project_url="https://github.com/thombashi/{}".format(PROJECT_NAME),
    )
    maker.examples_dir_name = "usage"

    maker.write_chapter("Summary")
    maker.write_introduction_file("summary.txt")
    maker.write_introduction_file("badges.txt")
    maker.write_introduction_file("feature.txt")

    write_examples(maker)

    maker.write_file(maker.doc_page_root_dir_path.joinpath("installation.rst"))

    maker.set_indent_level(0)
    maker.write_chapter("Documentation")
    maker.write_lines(["https://{:s}.rtfd.io/".format(PROJECT_NAME.lower())])

    return 0


if __name__ == "__main__":
    sys.exit(main())
