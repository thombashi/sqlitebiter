#!/usr/bin/env python
# encoding: utf-8

'''
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
'''

from __future__ import print_function, unicode_literals

import io
import os
import sys
from textwrap import indent

import sqlitebiter
from subprocrunner import SubprocessRunner


def main():
    formula_body = []

    with io.open(os.path.join("docs", "pages", "introduction", "summary.txt"), encoding="utf8") as f:
        formula_body.append('desc "{}"'.format(f.read().strip()))

    base_url = "https://github.com/thombashi/{pkg}/releases/download/v{version}".format(
        pkg=sqlitebiter.__name__, version=sqlitebiter.__version__)

    proc = SubprocessRunner("wget {base}/{pkg}_macos_sha256.txt -O -".format(
        base=base_url, pkg=sqlitebiter.__name__))
    if proc.run() != 0:
        print(proc.stderr, file=sys.stderr)
        return proc.returncode

    formula_body.extend([
        'homepage "https://github.com/thombashi/{}"'.format(sqlitebiter.__name__),
        'url "{bin_url}"'.format(bin_url="{base}/{pkg}_macos_amd64.tar.gz".format(
            base=base_url, pkg=sqlitebiter.__name__)),
        'version "{}"'.format(sqlitebiter.__version__),
        'sha256 "{sha256}"'.format(sha256=proc.stdout.split()[0]),
        '',
        'def install',
        '  bin.install "{}"'.format(sqlitebiter.__name__),
        'end',
    ])

    print("class Sqlitebiter < Formula")
    print(indent("\n".join(formula_body), "  "))
    print("end")

    return 0


if __name__ == '__main__':
    sys.exit(main())
