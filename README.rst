**sqlitebiter**

.. contents:: Table of Contents
   :depth: 2

Summary
=========
A CLI tool to convert CSV / Excel / HTML / JSON / Jupyter Notebook / LDJSON / LTSV / Markdown / SQLite / SSV / TSV / Google-Sheets to a SQLite database file.

.. image:: https://badge.fury.io/py/sqlitebiter.svg
    :target: https://badge.fury.io/py/sqlitebiter

.. image:: https://img.shields.io/pypi/pyversions/sqlitebiter.svg
   :target: https://pypi.python.org/pypi/sqlitebiter

.. image:: https://img.shields.io/travis/thombashi/sqlitebiter/master.svg?label=Linux/macOS
   :target: https://travis-ci.org/thombashi/sqlitebiter
   :alt: Linux CI test status

.. image:: https://img.shields.io/appveyor/ci/thombashi/sqlitebiter/master.svg?label=Windows
   :target: https://ci.appveyor.com/project/thombashi/sqlitebiter
   :alt: Windows CI test status

.. image:: https://img.shields.io/github/stars/thombashi/sqlitebiter.svg?style=social&label=Star
   :target: https://github.com/thombashi/sqlitebiter
   :alt: GitHub repository

Features
--------
- Create a SQLite database file from:
    - File(s):
        - CSV
        - Microsoft Excel :superscript:`TM`
        - HTML
        - JSON
        - `Jupyter Notebook <http://jupyter.org/>`__
        - `Labeled Tab-separated Values (LTSV) <http://ltsv.org/>`__
        - `Line-delimited JSON(LDJSON) <https://en.wikipedia.org/wiki/JSON_streaming#Line-delimited_JSON>`__/NDJSON/JSON Lines
        - Markdown
        - Mediawiki
        - Space separated values (SSV)
        - SQLite
        - Tab separated values (TSV)
    - `Google Sheets <https://www.google.com/intl/en_us/sheets/about/>`_
    - URL (scrape data from web pages)
- Multi-byte character support
- Automatic file encoding detection

Usage
=======
Create SQLite database from files
-----------------------------------
.. image:: docs/gif/usage_example.gif

Create SQLite database from URL
---------------------------------
Following is an example that convert HTML table tags within a web page to SQLite tables.

:Example:
    .. code-block:: console

        $ sqlitebiter url "https://en.wikipedia.org/wiki/Comparison_of_firewalls"
        [INFO] sqlitebiter url: convert 'Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html1' table
        [INFO] sqlitebiter url: convert 'Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html2' table
        [INFO] sqlitebiter url: convert 'Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html3' table
        [INFO] sqlitebiter url: convert 'Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html4' table
        [INFO] sqlitebiter url: convert 'Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html5' table
        [INFO] sqlitebiter url: convert 'Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html6' table
        [INFO] sqlitebiter url: convert 'Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html7' table
        [INFO] sqlitebiter url: convert 'Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html8' table
        [INFO] sqlitebiter url: convert 'Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html9' table
        [INFO] sqlitebiter url: convert 'Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html10' table
        [INFO] sqlitebiter url: convert 'Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html11' table
        [INFO] sqlitebiter url: converted results: source=1, success=11, created-table=11
        [INFO] sqlitebiter url: database path: /home/sqlitebiter/out.sqlite

:Output:
    .. code-block:: console

        sqlite> .schema
        CREATE TABLE IF NOT EXISTS '_source_info_' (source_id INTEGER NOT NULL, dir_name TEXT, base_name TEXT NOT NULL, format_name TEXT NOT NULL, dst_table TEXT NOT NULL, size INTEGER, mtime INTEGER);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html1' (Firewall TEXT, License TEXT, [Cost and usage limits] TEXT, OS TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html2' (Firewall TEXT, License TEXT, Cost TEXT, OS TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html3' ([Can Target:] TEXT, [Changing default policy to accept/reject (by issuing a single rule)] TEXT, [IP destination address(es)] TEXT, [IP source address(es)] TEXT, [TCP/UDP destination port(s)] TEXT, [TCP/UDP source port(s)] TEXT, [Ethernet MAC destination address] TEXT, [Ethernet MAC source address] TEXT, [Inbound firewall (ingress)] TEXT, [Outbound firewall (egress)] TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html4' ([Can:] TEXT, [work at OSI Layer 4 (stateful firewall)] TEXT, [work at OSI Layer 7 (application inspection)] TEXT, [Change TTL? (Transparent to traceroute)] TEXT, [Configure REJECT-with answer] TEXT, [DMZ (de-militarized zone) - allows for single/several hosts not to be firewalled.] TEXT, [Filter according to time of day] TEXT, [Redirect TCP/UDP ports (port forwarding)] TEXT, [Redirect IP addresses (forwarding)] TEXT, [Filter according to User Authorization] TEXT, [Traffic rate-limit / QoS] TEXT, Tarpit TEXT, Log TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html5' ([Features:] TEXT, "Configuration: GUI_ text or both modes?" TEXT, "Remote Access: Web (HTTP)_ Telnet_ SSH_ RDP_ Serial COM RS232_ ..." TEXT, [Change rules without requiring restart?] TEXT, [Ability to centrally manage all firewalls together] TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html6' ([Features:] TEXT, [Modularity: supports third-party modules to extend functionality?] TEXT, [IPS : Intrusion prevention system] TEXT, [Open-Source License?] TEXT, [supports IPv6 ?] TEXT, [Class: Home / Professional] TEXT, [Operating Systems on which it runs?] TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html7' ([Can:] TEXT, "NAT44 (static_ dynamic w/o ports_ PAT)" TEXT, "NAT64_ NPTv6" TEXT, [IDS (Intrusion Detection System)] TEXT, [VPN (Virtual Private Network)] TEXT, [AV (Anti-Virus)] TEXT, Sniffer TEXT, [Profile selection] TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html8' ("v_t_e___Firewall software" TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html9' (A TEXT, B TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html10' (A TEXT, B TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html11' (A TEXT, B TEXT);

For more information
~~~~~~~~~~~~~~~~~~~~~~
More examples are available at 
http://sqlitebiter.rtfd.io/en/latest/pages/usage/index.html

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


Bash Auto Completion
----------------------------------------------------------
.. code:: console

    $ wget https://raw.githubusercontent.com/thombashi/sqlitebiter/master/scripts/sqlitebiter-complete.sh -O - >> ~/.bash_profile
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

Documentation
===============
http://sqlitebiter.rtfd.io/

