#!/usr/bin/env python
# encoding: utf-8

import os
import sys


PROJECT_NAME = "sqlitebiter"
VERSION = "0.4.0"
OUTPUT_DIR = ".."
README_WORK_DIR = "."
DOC_PAGE_DIR = os.path.join(README_WORK_DIR, "pages")


def get_usage_file_path(filename):
    return os.path.join(DOC_PAGE_DIR, "examples", filename)


def write_line_list(f, line_list):
    f.write("\n".join(line_list))
    f.write("\n" * 2)


def write_usage_file(f, filename):
    write_line_list(f, [
        line.rstrip()
        for line in
        open(get_usage_file_path(filename)).readlines()
    ])


def write_examples(f):
    write_line_list(f, [
        "Usage",
        "========",
        "",
        ".. image:: docs/gif/usage_example.gif",
    ])

    write_line_list(f, [
        "For more information",
        "--------------------",
        "More examples are available at ",
        "http://%s.readthedocs.org/en/latest/pages/examples/index.html" % (
            PROJECT_NAME),
        "",
    ])


def main():
    with open(os.path.join(OUTPUT_DIR, "README.rst"), "w") as f:
        write_line_list(f, [
            PROJECT_NAME,
            "=============",
            "",
        ] + [
            line.rstrip() for line in
            open(os.path.join(
                DOC_PAGE_DIR, "introduction", "badges.txt")).readlines()
        ])

        write_line_list(f, [
            "Summary",
            "-------",
            "",
        ] + [
            line.rstrip() for line in
            open(os.path.join(
                DOC_PAGE_DIR, "introduction", "summary.txt")).readlines()
        ])

        write_line_list(f, [
            line.rstrip() for line in
            open(os.path.join(
                DOC_PAGE_DIR, "introduction", "feature.txt")).readlines()
        ])

        write_examples(f)

        write_line_list(f, [
            line.rstrip() for line in
            open(os.path.join(DOC_PAGE_DIR, "installation.rst")).readlines()
        ])

        write_line_list(f, [
            "Documentation",
            "=============",
            "",
            "http://%s.readthedocs.org/en/latest/" % (PROJECT_NAME)
        ])

    sys.stdout.write("complete\n")
    sys.stdout.flush()
    sys.stdin.readline()

if __name__ == '__main__':
    sys.exit(main())
