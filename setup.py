#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import io
import os.path
import sys

import setuptools
import sqlitebiter


MODULE_NAME = "sqlitebiter"
REPOSITORY_URL = "https://github.com/thombashi/{:s}".format(MODULE_NAME)
REQUIREMENT_DIR = "requirements"
ENCODING = "utf8"


def need_pytest():
    return set(["pytest", "test", "ptr"]).intersection(sys.argv)


pytest_runner = ["pytest-runner"] if need_pytest() else []


with io.open("README.rst", encoding=ENCODING) as fp:
    long_description = fp.read()

with io.open(os.path.join("docs", "pages", "introduction", "summary.txt"), encoding=ENCODING) as f:
    summary = f.read().strip()

with open(os.path.join(REQUIREMENT_DIR, "requirements.txt")) as f:
    install_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "test_requirements.txt")) as f:
    tests_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "build_requirements.txt")) as f:
    build_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "docs_requirements.txt")) as f:
    docs_requires = [line.strip() for line in f if line.strip()]

SETUPTOOLS_REQUIRES = ["setuptools>=38.3.0"]

setuptools.setup(
    name=MODULE_NAME,
    version=sqlitebiter.VERSION,
    url=REPOSITORY_URL,

    author="Tsuyoshi Hombashi",
    author_email="tsuyoshi.hombashi@gmail.com",
    description=summary,
    include_package_data=True,
    keywords=[
        "SQLite", "converter",
        "CSV", "Excel", "Google Sheets", "HTML", "JSON", "LTSV", "TSV",
    ],
    license="MIT License",
    long_description=long_description,
    packages=setuptools.find_packages(exclude=['test*']),
    project_urls={
        "Documentation": "http://{:s}.rtfd.io/".format(MODULE_NAME),
        "Tracker": "{:s}/issues".format(REPOSITORY_URL),
    },

    install_requires=SETUPTOOLS_REQUIRES + install_requires,
    setup_requires=SETUPTOOLS_REQUIRES + pytest_runner,
    tests_require=tests_requires,
    extras_require={
        "build": build_requires,
        "docs": docs_requires,
        "test": tests_requires,
    },
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*',

    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Database",
    ],
    entry_points={
        "console_scripts": [
            "sqlitebiter=sqlitebiter.sqlitebiter:cmd",
        ],
    })
