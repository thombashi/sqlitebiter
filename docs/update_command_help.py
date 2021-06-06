#!/usr/bin/env python3

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import os
import sys
from textwrap import dedent, indent

from subprocrunner import SubprocessRunner


def main() -> int:
    env = dict(os.environ, LC_ALL="C.UTF-8")

    proc = SubprocessRunner("sqlitebiter -h")
    proc.run(env=env, check=True)
    assert proc.stdout
    help_file_path = "pages/usage/help.txt"
    print(help_file_path)

    with open(help_file_path, "w") as f:
        f.write(
            dedent(
                """\
                ::

                """
            )
        )

        f.write(indent(proc.stdout, "    "))

    for subcommand in ["file", "gs", "url", "stdin"]:
        proc = SubprocessRunner(f"sqlitebiter {subcommand:s} -h")
        proc.run(env=env, check=True)
        assert proc.stdout
        help_file_path = f"pages/usage/{subcommand:s}/help.txt"

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

    return 0


if __name__ == "__main__":
    sys.exit(main())
