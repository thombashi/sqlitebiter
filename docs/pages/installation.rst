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

        $ wget https://github.com/thombashi/sqlitebiter/releases/download/v0.12.0/sqlitebiter_0.12.0_amd64.deb
        $ sudo dpkg -i sqlitebiter_0.12.0_amd64.deb


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
    Usage: sqlitebiter.exe [OPTIONS] COMMAND [ARGS]...

    Options:
      --version         Show the version and exit.
      -a, --append      append table(s) to existing database.
      -i, --index TEXT  comma separated attribute names to create indices.
      -v, --verbose
      --debug           for debug print.
      --quiet           suppress execution log messages.
      -h, --help        Show this message and exit.

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
- `nbformat <http://jupyter.org/>`__
- `logbook <http://logbook.readthedocs.io/en/stable/>`__
- `path.py <https://github.com/jaraco/path.py>`__
- `pytablereader <https://github.com/thombashi/pytablereader>`__
- `SimpleSQLite <https://github.com/thombashi/SimpleSQLite>`__
- `sqliteschema <https://github.com/thombashi/sqliteschema>`__
- `typepy <https://github.com/thombashi/typepy>`__

Google Sheets dependencies (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Following Python packages are required to 
`manual installation <http://sqlitebiter.readthedocs.io/en/latest/pages/usage/gs/index.html>`_ 
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
- `pytest <http://pytest.org/latest/>`__
- `pytest-runner <https://pypi.python.org/pypi/pytest-runner>`__
- `responses <https://github.com/getsentry/responses>`__
- `tox <https://testrun.org/tox/latest/>`__

Misc dependencies (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- `lxml <http://lxml.de/installation.html>`__
- `pypandoc <https://github.com/bebraw/pypandoc>`__
    - required when converting MediaWiki files


Dependencies other than Python packages (Optional)
------------------------------------------------------------
- ``libxml2`` (faster HTML/Markdown conversion)
- `pandoc <http://pandoc.org/>`__ (required when converting MediaWiki files)
