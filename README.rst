**sqlitebiter**

.. contents:: Table of Contents
   :depth: 2

Summary
=========
A CLI tool to convert CSV/Excel/HTML/JSON/LTSV/Markdown/SQLite/TSV/Google-Sheets to a SQLite database file.

.. image:: https://img.shields.io/travis/thombashi/sqlitebiter/master.svg?label=Linux
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
        - `Labeled Tab-separated Values (LTSV) <http://ltsv.org/>`__
        - Markdown
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

        $ sqlitebiter -v url "https://en.wikipedia.org/wiki/Comparison_of_firewalls"
        [INFO] sqlitebiter url: convert 'https://en.wikipedia.org/wiki/Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html1 (Firewall TEXT, License TEXT, Costandusagelimits TEXT, OS TEXT)' table
        [INFO] sqlitebiter url: convert 'https://en.wikipedia.org/wiki/Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html2 (Firewall TEXT, License TEXT, Cost TEXT, OS TEXT)' table
        [INFO] sqlitebiter url: convert 'https://en.wikipedia.org/wiki/Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html3 (CanTarget TEXT, Changingdefaultpolicytoacceptrejectbyissuingasinglerule TEXT, IPdestinationaddresses TEXT, IPsourceaddresses TEXT, TCPUDPdestinationports TEXT, TCPUDPsourceports TEXT, EthernetMACdestinationaddress TEXT, EthernetMACsourceaddress TEXT, Inboundfirewallingress TEXT, Outboundfirewallegress TEXT)' table
        [INFO] sqlitebiter url: convert 'https://en.wikipedia.org/wiki/Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html4 (Can TEXT, workatOSILayer4statefulfirewall TEXT, workatOSILayer7applicationinspection TEXT, ChangeTTLTransparenttotraceroute TEXT, ConfigureREJECTwithanswer TEXT, DMZdemilitarizedzoneallowsforsingleseveralhostsnottobefirewalled TEXT, Filteraccordingtotimeofday TEXT, RedirectTCPUDPportsportforwarding TEXT, RedirectIPaddressesforwarding TEXT, FilteraccordingtoUserAuthorization TEXT, TrafficratelimitQoS TEXT, Tarpit TEXT, Log TEXT)' table
        [INFO] sqlitebiter url: convert 'https://en.wikipedia.org/wiki/Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html5 (Features TEXT, ConfigurationGUItextorbothmodes TEXT, RemoteAccessWebHTTPTelnetSSHRDPSerialCOMRS232 TEXT, Changeruleswithoutrequiringrestart TEXT, Abilitytocentrallymanageallfirewallstogether TEXT)' table
        [INFO] sqlitebiter url: convert 'https://en.wikipedia.org/wiki/Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html6 (Features TEXT, Modularitysupportsthirdpartymodulestoextendfunctionality TEXT, IPS : Intrusion prevention system] TEXT, OpenSourceLicense TEXT, supports IPv6 ?] TEXT, ClassHomeProfessional TEXT, OperatingSystemsonwhichitruns TEXT)' table
        [INFO] sqlitebiter url: convert 'https://en.wikipedia.org/wiki/Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html7 (Can TEXT, NAT44staticdynamicwoportsPAT TEXT, NAT64NPTv6 TEXT, IDSIntrusionDetectionSystem TEXT, VPNVirtualPrivateNetwork TEXT, AVAntiVirus TEXT, Sniffer TEXT, Profileselection TEXT)' table
        [INFO] sqlitebiter url: convert 'https://en.wikipedia.org/wiki/Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html8 (vteFirewallsoftware TEXT)' table
        [INFO] sqlitebiter url: convert 'https://en.wikipedia.org/wiki/Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html9 (A TEXT, B TEXT)' table
        [INFO] sqlitebiter url: convert 'https://en.wikipedia.org/wiki/Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html10 (A TEXT, B TEXT)' table
        [INFO] sqlitebiter url: convert 'https://en.wikipedia.org/wiki/Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html11 (A TEXT, B TEXT)' table
        [INFO] sqlitebiter url: number of created tables: 11
        [INFO] sqlitebiter url: database path: out.sqlite

:Output:
    .. code-block:: console

        sqlite> .schema
        CREATE TABLE 'Comparison_of_firewalls_Wikipedia_html1' (Firewall TEXT, License TEXT, Costandusagelimits TEXT, OS TEXT);
        CREATE TABLE 'Comparison_of_firewalls_Wikipedia_html2' (Firewall TEXT, License TEXT, Cost TEXT, OS TEXT);
        CREATE TABLE 'Comparison_of_firewalls_Wikipedia_html3' (CanTarget TEXT, Changingdefaultpolicytoacceptrejectbyissuingasinglerule TEXT, IPdestinationaddresses TEXT, IPsourceaddresses TEXT, TCPUDPdestinationports TEXT, TCPUDPsourceports TEXT, EthernetMACdestinationaddress TEXT, EthernetMACsourceaddress TEXT, Inboundfirewallingress TEXT, Outboundfirewallegress TEXT);
        CREATE TABLE 'Comparison_of_firewalls_Wikipedia_html4' (Can TEXT, [workatOSILayer4statefulfirewall] TEXT, [workatOSILayer7applicationinspection] TEXT, ChangeTTLTransparenttotraceroute TEXT, ConfigureREJECTwithanswer TEXT, DMZdemilitarizedzoneallowsforsingleseveralhostsnottobefirewalled TEXT, Filteraccordingtotimeofday TEXT, RedirectTCPUDPportsportforwarding TEXT, RedirectIPaddressesforwarding TEXT, FilteraccordingtoUserAuthorization TEXT, TrafficratelimitQoS TEXT, Tarpit TEXT, Log TEXT);
        CREATE TABLE 'Comparison_of_firewalls_Wikipedia_html5' (Features TEXT, ConfigurationGUItextorbothmodes TEXT, [RemoteAccessWebHTTPTelnetSSHRDPSerialCOMRS232] TEXT, Changeruleswithoutrequiringrestart TEXT, Abilitytocentrallymanageallfirewallstogether TEXT);
        CREATE TABLE 'Comparison_of_firewalls_Wikipedia_html6' (Features TEXT, Modularitysupportsthirdpartymodulestoextendfunctionality TEXT, [IPS : Intrusion prevention system] TEXT, OpenSourceLicense TEXT, [supports IPv6 ?] TEXT, ClassHomeProfessional TEXT, OperatingSystemsonwhichitruns TEXT);
        CREATE TABLE 'Comparison_of_firewalls_Wikipedia_html7' (Can TEXT, [NAT44staticdynamicwoportsPAT] TEXT, [NAT64NPTv6] TEXT, IDSIntrusionDetectionSystem TEXT, VPNVirtualPrivateNetwork TEXT, AVAntiVirus TEXT, Sniffer TEXT, Profileselection TEXT);
        CREATE TABLE 'Comparison_of_firewalls_Wikipedia_html9' (A TEXT, B TEXT);
        CREATE TABLE 'Comparison_of_firewalls_Wikipedia_html10' (A TEXT, B TEXT);
        CREATE TABLE 'Comparison_of_firewalls_Wikipedia_html11' (A TEXT, B TEXT);

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


Dependencies
============
Python 2.7+ or 3.4+

Python package dependencies are as follows.

Mandatory Python package dependencies
------------------------------------------------------------
Following mandatory Python packages are automatically installed during
``sqlitebiter`` installation process:

- `appconfigpy <https://github.com/thombashi/appconfigpy>`__
- `click <http://click.pocoo.org/>`__
- `logbook <http://logbook.readthedocs.io/en/stable/>`__
- `path.py <https://github.com/jaraco/path.py>`__
- `pytablereader <https://github.com/thombashi/pytablereader>`__
- `SimpleSQLite <https://github.com/thombashi/SimpleSQLite>`__
- `sqliteschema <https://github.com/thombashi/sqliteschema>`__
- `typepy <https://github.com/thombashi/typepy>`__

Google Sheets dependencies (Optional)
------------------------------------------------------------
Following Python packages are required to
`manual installation <http://sqlitebiter.readthedocs.io/en/latest/pages/usage/gs/index.html>`_
when you use Google Sheets feature:

- `gspread <https://github.com/burnash/gspread>`_
- `oauth2client <https://github.com/google/oauth2client/>`_
- `pyOpenSSL <https://pyopenssl.readthedocs.io/en/stable/>`_

Test dependencies
------------------------------------------------------------
- `pytablewriter <https://github.com/thombashi/pytablewriter>`__
- `pytest <http://pytest.org/latest/>`__
- `pytest-runner <https://pypi.python.org/pypi/pytest-runner>`__
- `tox <https://testrun.org/tox/latest/>`__

Misc
------------------------------------------------------------
- `lxml <http://lxml.de/installation.html>`__ (Faster HTML convert if installed)

Documentation
===============
http://sqlitebiter.rtfd.io/

