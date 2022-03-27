#!/usr/bin/env python3

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import os
import sys
from textwrap import indent

import retryrequests

import sqlitebiter


def fetch_checksum(base_url: str, exec_bin_filename: str) -> str:
    response = retryrequests.get(f"{base_url}/sqlitebiter_sha256.txt")
    response.raise_for_status()
    for line in response.text.splitlines():
        if exec_bin_filename in line:
            return line.split()[0]

    print(f"[ERROR] checksum not found of {exec_bin_filename}", file=sys.stderr)
    sys.exit(2)


def main() -> int:
    formula_body = []

    with open(os.path.join("docs", "pages", "introduction", "summary.txt"), encoding="utf8") as f:
        formula_body.append(f'desc "{f.read().strip()}"')

    base_url = "https://github.com/thombashi/{pkg}/releases/download/v{version}".format(
        pkg=sqlitebiter.__name__, version=sqlitebiter.__version__
    )
    exec_bin_filename = f"{sqlitebiter.__name__}_macos_amd64.tar.gz"

    exec_bin_url = f"{base_url}/{exec_bin_filename}"
    response = retryrequests.head(exec_bin_url)
    response.raise_for_status()

    formula_body.extend(
        [
            f'homepage "https://github.com/thombashi/{sqlitebiter.__name__}"',
            f'url "{exec_bin_url}"',
            f'version "{sqlitebiter.__version__}"',
            f'sha256 "{fetch_checksum(base_url, exec_bin_filename)}"',
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
