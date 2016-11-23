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
    - file(s):
        - CSV
        - Microsoft Excel :superscript:`TM`
        - HTML: extract table tag data
        - JSON
        - Markdown: extract Markdown table
    - `Google Sheets <https://www.google.com/intl/en_us/sheets/about/>`_
    - URL (fetch data from the Internet)
- Multi-byte character support

Usage
=====

Create SQLite database from files
---------------------------------

.. image:: docs/gif/usage_example.gif

Create SQLite database from URL
-------------------------------

Convert HTML table tags within a web page to SQLite tables.

.. code:: console

    $ sqlitebiter url https://en.wikipedia.org/wiki/List_of_unit_testing_frameworks
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html1' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html2' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html3' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html4' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html5' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html6' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html7' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html8' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html9' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html10' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html11' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html12' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html13' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html14' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html15' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html16' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html18' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html19' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html20' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html21' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html22' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html23' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html24' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html25' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html26' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html27' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html28' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html29' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html30' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html31' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html32' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html33' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html34' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html35' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html36' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html37' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html38' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html39' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html40' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html41' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html42' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html43' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html44' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html45' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html46' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html47' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html48' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html49' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html50' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html51' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html52' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html53' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html54' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html55' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html56' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html57' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html58' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html59' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html60' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html61' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html62' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html63' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html64' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html65' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html66' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html67' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html68' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html69' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html70' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html71' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html72' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html73' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html74' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html75' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html76' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html77' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html78' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html79' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html80' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html81' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html82' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html83' table
    convert a table to 'List_of_unit_testing_frameworks_Wikipedia_html84' table

Output SQLite database has following table structure:


.. code:: console

    List_of_unit_testing_frameworks_Wikipedia_html1 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html2 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html3 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html4 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html5 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html6 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html7 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html8 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html9 (Name TEXT, xUnit TEXT, Fixtures TEXT, Groupfixtures TEXT, Generators TEXT, Source TEXT, License TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html10 (Name TEXT, License TEXT, xUnit TEXT, Fixtures TEXT, Groupfixtures TEXT, Generators TEXT, Mocks TEXT, Exceptions TEXT, Macros TEXT, Templates TEXT, Grouping TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html11 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html12 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html13 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html14 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html15 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html16 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html18 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html19 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html20 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html21 (Name TEXT, xUnit TEXT, Fixtures TEXT, GroupFixtures TEXT, Generators TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html22 (Name TEXT, xUnit TEXT, Fixtures TEXT, Groupfixtures TEXT, Generators TEXT, MPI TEXT, OpenMP TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html23 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html24 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html25 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html26 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html27 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html28 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html29 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html30 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html31 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html32 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html33 (Name TEXT, xUnit TEXT, TAP TEXT, Clientside TEXT, Serverside TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html34 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html35 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html36 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html37 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html38 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html39 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html40 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html41 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html42 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html43 (Name TEXT, xUnit TEXT, TAP TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html44 (Name TEXT, xUnit TEXT, TAP TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html45 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html46 (Name TEXT, xUnit TEXT, TAP TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html47 (Name TEXT, xUnit TEXT, TAP TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html48 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html49 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html50 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html51 (Name TEXT, xUnit TEXT, Generators TEXT, Fixtures TEXT, GroupFixtures TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html52 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html53 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html54 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html55 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html56 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html57 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html58 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html59 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html60 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html61 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html62 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html63 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html64 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html65 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html66 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html67 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT, Active TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html68 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT, Active TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html69 (Name TEXT, xUnit TEXT, TAP TEXT, Source TEXT, Remarks TEXT, Active TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html70 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html71 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html72 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html73 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html74 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html75 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html76 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html77 (Name TEXT, Source TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html78 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html79 (Name TEXT, xUnit TEXT, License TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html80 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html81 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html82 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html83 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)
    List_of_unit_testing_frameworks_Wikipedia_html84 (Name TEXT, xUnit TEXT, Source TEXT, Remarks TEXT)


For more information
~~~~~~~~~~~~~~~~~~~~

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
- `sqlitestructure <https://github.com/thombashi/sqlitestructure>`__


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

