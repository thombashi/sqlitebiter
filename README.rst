sqlitebiter
=============

.. image:: https://img.shields.io/pypi/pyversions/sqlitebiter.svg
   :target: https://pypi.python.org/pypi/sqlitebiter
.. image:: https://travis-ci.org/thombashi/sqlitebiter.svg?branch=master
    :target: https://travis-ci.org/thombashi/sqlitebiter

Summary
-------

sqlitebiter is a CLI tool to create a SQLite database from CSV/JSON/Excel/Google-Sheets.

Features
--------

- Create a SQLite database file from:
    - CSV file(s)
    - JSON file(s)
    - Microsoft Excel :superscript:`TM` file(s)
    - `Google Sheets <https://www.google.com/intl/en_us/sheets/about/>`_

Usage
========

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

Python packages
---------------

Dependency python packages are automatically installed during
``sqlitebiter`` installation via pip.

- `click <http://click.pocoo.org/>`__
- `DataPropery <https://github.com/thombashi/DataProperty>`__
- `path.py <https://github.com/jaraco/path.py>`__
- `SimpleSQLite <https://github.com/thombashi/SimpleSQLite>`__

Google Sheets dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Google Sheets dependency packages are required some manual installation.

- `oauth2client <https://github.com/google/oauth2client/>`_
- `pyOpenSSL <https://pyopenssl.readthedocs.io/en/stable/>`_

Test dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `pytest <http://pytest.org/latest/>`__
- `pytest-runner <https://pypi.python.org/pypi/pytest-runner>`__
- `tox <https://testrun.org/tox/latest/>`__
- `XlsxWriter <http://xlsxwriter.readthedocs.io/>`__

Documentation
=============

http://sqlitebiter.readthedocs.org/en/latest/

