sqlitebiter
===========

.. image:: https://img.shields.io/pypi/pyversions/sqlitebiter.svg
   :target: https://pypi.python.org/pypi/sqlitebiter

.. image:: https://img.shields.io/travis/thombashi/sqlitebiter/master.svg?label=Linux
    :target: https://travis-ci.org/thombashi/sqlitebiter
    :alt: Linux CI test status

.. image:: https://img.shields.io/appveyor/ci/thombashi/sqlitebiter/master.svg?label=Windows
    :target: https://ci.appveyor.com/project/thombashi/sqlitebiter
    :alt: Windows CI test status

Summary
-------

sqlitebiter is a CLI tool to convert CSV/Excel/HTML/JSON/Markdown/Google-Sheets to a SQLite database file.

Features
--------

- Create a SQLite database file from:
    - CSV file(s)
    - Microsoft Excel :superscript:`TM` file(s)
    - HTML file(s): extract table tag data
    - JSON file(s)
    - Markdown file(s): extract Markdown table
    - `Google Sheets <https://www.google.com/intl/en_us/sheets/about/>`_

Usage
=====

.. image:: docs/gif/usage_example.gif

For more information
--------------------

More examples are available at 
http://sqlitebiter.readthedocs.io/en/latest/pages/usage/index.html

Installation
============

Install via pip
---------------

``sqlitebiter`` can be installed via
`pip <https://pip.pypa.io/en/stable/installing/>`__ (Python package manager).

.. code:: console

    sudo pip install sqlitebiter


Dependencies
============

Python packages (mandatory)
------------------------------
Dependency python packages are automatically installed during
``sqlitebiter`` installation via ``pip``.

- `click <http://click.pocoo.org/>`__
- `DataPropery <https://github.com/thombashi/DataProperty>`__
- `logbook <http://logbook.readthedocs.io/en/stable/>`__
- `path.py <https://github.com/jaraco/path.py>`__
- `pytablereader <https://github.com/thombashi/pytablereader>`__
- `SimpleSQLite <https://github.com/thombashi/SimpleSQLite>`__


Google Sheets dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Manual installation <http://sqlitebiter.readthedocs.io/en/latest/pages/usage/gs/index.html>`_ required to use Google Sheets feature.

- `oauth2client <https://github.com/google/oauth2client/>`_
- `pyOpenSSL <https://pyopenssl.readthedocs.io/en/stable/>`_


Test dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `pytest <http://pytest.org/latest/>`__
- `pytest-runner <https://pypi.python.org/pypi/pytest-runner>`__
- `tox <https://testrun.org/tox/latest/>`__
- `XlsxWriter <http://xlsxwriter.readthedocs.io/>`__

Python packages (optional)
------------------------------
- `lxml <http://lxml.de/installation.html>`__ (Faster HTML convert if installed)


Documentation
=============

http://sqlitebiter.readthedocs.org/en/latest/

