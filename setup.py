"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import os.path
from typing import Dict, Type

import setuptools


MODULE_NAME = "sqlitebiter"
REPOSITORY_URL = f"https://github.com/thombashi/{MODULE_NAME:s}"
REQUIREMENT_DIR = "requirements"
ENCODING = "utf8"

pkg_info: Dict[str, str] = {}


def get_release_command_class() -> Dict[str, Type[setuptools.Command]]:
    try:
        from releasecmd import ReleaseCommand
    except ImportError:
        return {}

    return {"release": ReleaseCommand}


with open(os.path.join(MODULE_NAME, "__version__.py")) as f:
    exec(f.read(), pkg_info)

with open("README.rst", encoding=ENCODING) as fp:
    long_description = fp.read()

with open(os.path.join("docs", "pages", "introduction", "summary.txt"), encoding=ENCODING) as f:
    summary = f.read().strip()

with open(os.path.join(REQUIREMENT_DIR, "requirements.txt")) as f:
    install_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "test_requirements.txt")) as f:
    tests_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "docs_requirements.txt")) as f:
    docs_requires = [line.strip() for line in f if line.strip()]

build_exe_requires = ["pyinstaller>=4.10"]
gs_requires = ["gspread", "oauth2client", "pyOpenSSL"]
mediawiki_requires = ["pypandoc"]
optional_requires = ["ujson>=1.33,<6"]

all_requires = gs_requires + mediawiki_requires + optional_requires
tests_requires = list(set(tests_requires + all_requires))

setuptools.setup(
    name=MODULE_NAME,
    version=pkg_info["__version__"],
    url=REPOSITORY_URL,
    author=pkg_info["__author__"],
    author_email=pkg_info["__email__"],
    description=summary,
    include_package_data=True,
    keywords=[
        "SQLite",
        "converter",
        "CSV",
        "Excel",
        "Google Sheets",
        "HTML",
        "JSON",
        "LTSV",
        "TSV",
    ],
    license=pkg_info["__license__"],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=setuptools.find_packages(exclude=["test*"]),
    project_urls={
        "Documentation": f"https://{MODULE_NAME:s}.rtfd.io/",
        "Download": f"{REPOSITORY_URL:s}/releases",
        "Source": REPOSITORY_URL,
        "Tracker": f"{REPOSITORY_URL:s}/issues",
        "Changlog": f"{REPOSITORY_URL:s}/releases",
    },
    python_requires=">=3.7",
    install_requires=install_requires,
    extras_require={
        "all": all_requires,
        "buildexe": build_exe_requires,
        "docs": docs_requires + all_requires,
        "gs": gs_requires,
        "mediawiki": mediawiki_requires,
        "test": tests_requires,
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Framework :: Jupyter",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Database",
    ],
    entry_points={"console_scripts": ["sqlitebiter=sqlitebiter.__main__:cmd"]},
    cmdclass=get_release_command_class(),
)
