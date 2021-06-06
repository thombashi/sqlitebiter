#!/usr/bin/env python3

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import os
import sys
from textwrap import indent

import retryrequests

import sqlitebiter


def main() -> int:
    formula_body = []

    with open(os.path.join("docs", "pages", "introduction", "summary.txt"), encoding="utf8") as f:
        formula_body.append(f'desc "{f.read().strip()}"')

    base_url = "https://github.com/thombashi/{pkg}/releases/download/v{version}".format(
        pkg=sqlitebiter.__name__, version=sqlitebiter.__version__
    )
    response = retryrequests.get(f"{base_url}/{sqlitebiter.__name__}_macos_sha256.txt")
    response.raise_for_status()

    formula_body.extend(
        [
            f'homepage "https://github.com/thombashi/{sqlitebiter.__name__}"',
            'url "{bin_url}"'.format(
                bin_url="{base}/{pkg}_macos_amd64.tar.gz".format(
                    base=base_url, pkg=sqlitebiter.__name__
                )
            ),
            f'version "{sqlitebiter.__version__}"',
            f'sha256 "{response.text.split()[0]}"',
            "",
            "def install",
            f'  bin.install "{sqlitebiter.__name__}"',
            "end",
        ]
    )

    print("class Sqlitebiter < Formula")
    print(indent("\n".join(formula_body), "  "))
    print("end")

    return 0


if __name__ == "__main__":
    sys.exit(main())
