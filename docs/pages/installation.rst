Installation
============

Install via pip (recommended)
------------------------------
``sqlitebiter`` can be installed via
`pip <https://pip.pypa.io/en/stable/installing/>`__ (Python package manager).

:Example:
    .. code:: console

        pip install sqlitebiter


Installation for Debian/Ubuntu from a deb package
----------------------------------------------------------
#. ``wget https://github.com/thombashi/sqlitebiter/releases/download/<version>/sqlitebiter_<version>_amd64.deb``
#. ``dpkg -iv sqlitebiter_<version>_amd64.deb``

:Example:
    .. code:: console

        $ wget https://github.com/thombashi/sqlitebiter/releases/download/v0.20.0/sqlitebiter_0.20.0_amd64.deb
        $ sudo dpkg -i sqlitebiter_0.20.0_amd64.deb


Installing executable files in Windows
----------------------------------------------------------
``sqlitebiter`` can be used in Windows environments without Python installation as follows:

#. Navigate to https://github.com/thombashi/sqlitebiter/releases
#. Download the latest version of the ``sqlitebiter_win_x64.zip``
#. Unzip the file
#. Execute ``sqlitebiter.exe`` in either Command Prompt or PowerShell

.. code-block:: batch

    >cd sqlitebiter_win_x64
    >sqlitebiter.exe -h
    Usage: sqlitebiter [OPTIONS] COMMAND [ARGS]...

    Options:
      --version               Show the version and exit.
      -o, --output-path PATH  Output path of the SQLite database file. Defaults to
                              'out.sqlite'.
      -a, --append            append table(s) to existing database.
      -i, --index TEXT        comma separated attribute names to create indices.
      --replace-symbol TEXT   Replace symbols in attributes.
      -v, --verbose
      --debug                 for debug print.
      -q, --quiet             suppress execution log messages.
      -h, --help              Show this message and exit.

    Commands:
      configure  Configure the following application settings:...
      file       Convert tabular data within...
      gs         Convert a spreadsheet in Google Sheets to a...
      url        Scrape tabular data from a URL and convert...


Installation for macOS via Homebrew
----------------------------------------------------------

.. code:: console

    $ brew tap thombashi/sqlitebiter
    $ brew install sqlitebiter

- `Homebrew Formula <https://github.com/thombashi/homebrew-sqlitebiter>`__


Command Completion for bash
----------------------------------------------------------
.. code:: console

    $ sqlitebiter completion >> ~/.bash_profile
    $ source ~/.bash_profile


Dependencies
============
Python 2.7+ or 3.4+

Python package dependencies are as follows.

Python package dependencies
------------------------------------------------------------

Mandatory dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Following mandatory Python packages are automatically installed during
``sqlitebiter`` installation process:

- `appconfigpy <https://github.com/thombashi/appconfigpy>`__
- `click <http://click.pocoo.org/>`__
- `colorama <https://github.com/tartley/colorama>`__
- `logbook <https://logbook.readthedocs.io/en/stable/>`__
- `msgfy <https://github.com/thombashi/msgfy>`__
- `nbformat <https://jupyter.org/>`__
- `path.py <https://github.com/jaraco/path.py>`__
- `pathvalidate <https://github.com/thombashi/pathvalidate>`__
- `pytablereader <https://github.com/thombashi/pytablereader>`__
- `SimpleSQLite <https://github.com/thombashi/SimpleSQLite>`__
- `typepy <https://github.com/thombashi/typepy>`__

Google Sheets dependencies (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Following Python packages are required to
`manual installation <https://sqlitebiter.readthedocs.io/en/latest/pages/usage/gs/index.html>`_
when you use Google Sheets feature:

- `gspread <https://github.com/burnash/gspread>`_
- `oauth2client <https://github.com/google/oauth2client/>`_
- `pyOpenSSL <https://pyopenssl.readthedocs.io/en/stable/>`_

The above packages can be installed with the following pip command;

.. code:: console

    $ pip install sqlitebiter[gs]

Test dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- `pytablewriter <https://github.com/thombashi/pytablewriter>`__
- `pytest <https://docs.pytest.org/en/latest/>`__
- `pytest-runner <https://github.com/pytest-dev/pytest-runner>`__
- `responses <https://github.com/getsentry/responses>`__
- `sqliteschema <https://github.com/thombashi/sqliteschema>`__
- `tox <https://testrun.org/tox/latest/>`__

Misc dependencies (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- `lxml <https://lxml.de/installation.html>`__
- `pypandoc <https://github.com/bebraw/pypandoc>`__
    - required when converting MediaWiki files


Dependencies other than Python packages (Optional)
------------------------------------------------------------
- ``libxml2`` (faster HTML/Markdown conversion)
- `pandoc <https://pandoc.org/>`__ (required when converting MediaWiki files)
