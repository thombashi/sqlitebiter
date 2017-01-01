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

sqlitebiter is a CLI tool to convert CSV/Excel/HTML/JSON/LTSV/Markdown/TSV/Google-Sheets to a SQLite database file.

Features
--------

- Create a SQLite database file from:
    - file(s):
        - CSV
        - Microsoft Excel :superscript:`TM`
        - HTML: extract table tag data
        - JSON
        - `Labeled Tab-separated Values (LTSV) <http://ltsv.org/>`__
        - Markdown: extract Markdown table
        - Tab separated values (TSV)
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

Following is an example that convert HTML table tags within a web page to SQLite tables.

.. code:: console

    $ sqlitebiter -v url "https://en.wikipedia.org/wiki/Comparison_of_firewalls"
    [INFO] convert 'https://en.wikipedia.org/wiki/Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html1 (Firewall TEXT, License TEXT, CostUsageLimits TEXT, OS TEXT)' table
    [INFO] convert 'https://en.wikipedia.org/wiki/Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html2 (Firewall TEXT, License TEXT, Cost TEXT, OS TEXT)' table
    [INFO] convert 'https://en.wikipedia.org/wiki/Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html3 (CanTarget TEXT, Changingdefaultpolicytoacceptrejectbyissuingasinglerule TEXT, IPdestinationaddresses TEXT, IPsourceaddresses TEXT, TCPUDPdestinationports TEXT, TCPUDPsourceports TEXT, EthernetMACdestinationaddress TEXT, EthernetMACsourceaddress TEXT, Inboundfirewallingress TEXT, Outboundfirewallegress TEXT)' table
    [INFO] convert 'https://en.wikipedia.org/wiki/Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html4 (Can TEXT, [workatOSILayer4statefulfirewall] TEXT, [workatOSILayer7applicationinspection] TEXT, ChangeTTLTransparenttotraceroute TEXT, ConfigureREJECTwithanswer TEXT, DMZdemilitarizedzoneallowsforsingleseveralhostsnottobefirewalled TEXT, Filteraccordingtotimeofday TEXT, RedirectTCPUDPportsportforwarding TEXT, RedirectIPaddressesforwarding TEXT, FilteraccordingtoUserAuthorization TEXT, TrafficratelimitQoS TEXT, Tarpit TEXT, Log TEXT)' table
    [INFO] convert 'https://en.wikipedia.org/wiki/Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html5 (Features TEXT, ConfigurationGUItextorbothmodes TEXT, [RemoteAccessWebHTTPTelnetSSHRDPSerialCOMRS232] TEXT, Changeruleswithoutrequiringrestart TEXT, Abilitytocentrallymanageallfirewallstogether TEXT)' table
    [INFO] convert 'https://en.wikipedia.org/wiki/Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html6 (Features TEXT, Modularitysupportsthirdpartymodulestoextendfunctionality TEXT, [IPS : Intrusion prevention system] TEXT, OpenSourceLicense TEXT, [supports IPv6 ?] TEXT, ClassHomeProfessional TEXT, OperatingSystemsonwhichitruns TEXT)' table
    [INFO] convert 'https://en.wikipedia.org/wiki/Comparison_of_firewalls' to 'Comparison_of_firewalls_Wikipedia_html7 (Can TEXT, [NAT44staticdynamicwoportsPAT] TEXT, [NAT64NPTv6] TEXT, IDSIntrusionDetectionSystem TEXT, VPNVirtualPrivateNetwork TEXT, AVAntiVirus TEXT, Sniffer TEXT, Profileselection TEXT)' table

For more information
~~~~~~~~~~~~~~~~~~~~

More examples are available at 
http://sqlitebiter.rtfd.io/en/latest/pages/usage/index.html

Installation
============

Install via pip (recommended)
------------------------------

``sqlitebiter`` can be installed via
`pip <https://pip.pypa.io/en/stable/installing/>`__ (Python package manager).

.. code:: console

    sudo pip install sqlitebiter

Python package dependencies are as follows.

Mandatory Python package dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Mandatory Python packages are automatically installed during
``sqlitebiter`` installation via ``pip``.

- `click <http://click.pocoo.org/>`__
- `DataPropery <https://github.com/thombashi/DataProperty>`__
- `logbook <http://logbook.readthedocs.io/en/stable/>`__
- `path.py <https://github.com/jaraco/path.py>`__
- `pytablereader <https://github.com/thombashi/pytablereader>`__
- `SimpleSQLite <https://github.com/thombashi/SimpleSQLite>`__
- `sqliteschema <https://github.com/thombashi/sqliteschema>`__

Google Sheets dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
`Manual installation <http://sqlitebiter.readthedocs.io/en/latest/pages/usage/gs/index.html>`_ required to use Google Sheets feature.

- `oauth2client <https://github.com/google/oauth2client/>`_
- `pyOpenSSL <https://pyopenssl.readthedocs.io/en/stable/>`_

Test dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- `pytest <http://pytest.org/latest/>`__
- `pytest-runner <https://pypi.python.org/pypi/pytest-runner>`__
- `tox <https://testrun.org/tox/latest/>`__
- `XlsxWriter <http://xlsxwriter.readthedocs.io/>`__

Misc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- `lxml <http://lxml.de/installation.html>`__ (Faster HTML convert if installed)


Installing executable file in Windows
--------------------------------------------
#. Navigate to https://github.com/thombashi/sqlitebiter/releases
#. Download the latest version of the ``sqlitebiter_win_x64.zip``
#. Unzip the file


Documentation
=============

http://sqlitebiter.rtfd.io/

