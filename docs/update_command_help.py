#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import print_function, unicode_literals

import os
from textwrap import dedent, indent

from subprocrunner import SubprocessRunner


for subcommand in ["file", "gs", "url"]:
    proc = SubprocessRunner("sqlitebiter {:s} -h".format(subcommand))
    proc.run(env=dict(os.environ, LC_ALL="C.UTF-8"))
    help_file_path = "pages/usage/{:s}/help.txt".format(subcommand)

    print(help_file_path)

    with open(help_file_path, "w") as f:
        f.write(
            dedent(
                """\
            ``sqlitebiter {:s}`` subcommand help
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            ::

            """.format(
                    subcommand
                )
            )
        )

        f.write(indent(proc.stdout, "    "))
