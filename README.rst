.. contents:: **sqlitebiter**
   :backlinks: top
   :depth: 2

Summary
=========
`sqlitebiter <https://github.com/thombashi/sqlitebiter>`__ is a CLI tool to convert CSV / Excel / HTML / JSON / Jupyter Notebook / LDJSON / LTSV / Markdown / SQLite / SSV / TSV / Google-Sheets to a SQLite database file.

.. image:: https://badge.fury.io/py/sqlitebiter.svg
    :target: https://badge.fury.io/py/sqlitebiter
    :alt: PyPI package version

.. image:: https://img.shields.io/pypi/pyversions/sqlitebiter.svg
    :target: https://pypi.org/project/sqlitebiter
    :alt: Supported Python versions

.. image:: https://img.shields.io/travis/thombashi/sqlitebiter/master.svg?label=Linux/macOS%20CI
   :target: https://travis-ci.org/thombashi/sqlitebiter
   :alt: Linux/macOS CI status

.. image:: https://img.shields.io/appveyor/ci/thombashi/sqlitebiter/master.svg?label=Windows%20CI
   :target: https://ci.appveyor.com/project/thombashi/sqlitebiter
   :alt: Windows CI status

.. image:: https://img.shields.io/github/stars/thombashi/sqlitebiter.svg?style=social&label=Star
    :target: https://github.com/thombashi/sqlitebiter
    :alt: GitHub stars

Features
--------
- Create a SQLite database file from:
    - File(s):
        - CSV / Tab separated values (TSV) / Space separated values (SSV)
        - Microsoft Excel :superscript:`TM`
        - HTML
        - JSON
        - `Jupyter Notebook <https://jupyter.org/>`__
        - `Labeled Tab-separated Values (LTSV) <http://ltsv.org/>`__
        - `Line-delimited JSON(LDJSON) <https://en.wikipedia.org/wiki/JSON_streaming#Line-delimited_JSON>`__ / NDJSON / JSON Lines
        - Markdown
        - Mediawiki
        - SQLite
    - `Google Sheets <https://www.google.com/intl/en_us/sheets/about/>`_
    - URL (scrape tabular data from web pages)
- Multi-byte character support
- Automatic file encoding detection

Usage
=======
Create SQLite database from files
-----------------------------------
.. image:: https://cdn.rawgit.com/thombashi/sqlitebiter/master/docs/svg/usage_example.svg

Create SQLite database from URL
---------------------------------
Following is an example that converts HTML table tags within a web page to SQLite tables by the web page URL.

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
        [INFO] sqlitebiter url: database path: out.sqlite

:Output:
    .. code-block:: sql

        $ sqlite3 out.sqlite .schema
        CREATE TABLE IF NOT EXISTS '_source_info_' ("source_id" INTEGER NOT NULL, "dir_name" TEXT, "base_name" TEXT NOT NULL, "format_name" TEXT NOT NULL, "dst_table" TEXT NOT NULL, size INTEGER, mtime INTEGER);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html1' (Firewall TEXT, License TEXT, [Cost and usage limits] TEXT, OS TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html2' (Firewall TEXT, License TEXT, Cost TEXT, OS TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html3' ([Can Target:] TEXT, [Changing default policy to accept/reject (by issuing a single rule)] TEXT, [IP destination address(es)] TEXT, [IP source address(es)] TEXT, [TCP/UDP destination port(s)] TEXT, [TCP/UDP source port(s)] TEXT, [Ethernet MAC destination address] TEXT, [Ethernet MAC source address] TEXT, [Inbound firewall (ingress)] TEXT, [Outbound firewall (egress)] TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html4' ([Can:] TEXT, [work at OSI Layer 4 (stateful firewall)] TEXT, [work at OSI Layer 7 (application inspection)] TEXT, [Change TTL? (Transparent to traceroute)] TEXT, [Configure REJECT-with answer] TEXT, [DMZ (de-militarized zone) - allows for single/several hosts not to be firewalled.] TEXT, [Filter according to time of day] TEXT, [Redirect TCP/UDP ports (port forwarding)] TEXT, [Redirect IP addresses (forwarding)] TEXT, [Filter according to User Authorization] TEXT, [Traffic rate-limit / QoS] TEXT, Tarpit TEXT, Log TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html5' ([Features:] TEXT, "Configuration: GUI_ text or both modes?" TEXT, "Remote Access: Web (HTTP)_ Telnet_ SSH_ RDP_ Serial COM RS232_ ..." TEXT, [Change rules without requiring restart?] TEXT, [Ability to centrally manage all firewalls together] TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html6' ([Features:] TEXT, [Modularity: supports third-party modules to extend functionality?] TEXT, [IPS : Intrusion prevention system] TEXT, [Open-Source License?] TEXT, [supports IPv6 ?] TEXT, [Class: Home / Professional] TEXT, [Operating Systems on which it runs?] TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html7' ([Can:] TEXT, "NAT44 (static_ dynamic w/o ports_ PAT)" TEXT, "NAT64_ NPTv6" TEXT, [IDS (Intrusion Detection System)] TEXT, [VPN (Virtual Private Network)] TEXT, [AV  (Anti-Virus)] TEXT, Sniffer TEXT, [Profile selection] TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html8' ([vteFirewall software] TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html9' (A TEXT, B TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html10' (A TEXT, B TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html11' (A TEXT, B TEXT);

The attributes within the converted SQLite database may include symbols as the above.
Symbols within attributes can be replaced by using ``--replace-symbol`` option.
In the following example shows replace symbols to underscores.

:Example:
    .. code-block:: console

        $ sqlitebiter --replace-symbol _ -q url "https://en.wikipedia.org/wiki/Comparison_of_firewalls"

:Output:
    .. code-block:: sql

        $ sqlite3 out.sqlite .schema
        CREATE TABLE IF NOT EXISTS '_source_info_' ("source_id" INTEGER NOT NULL, "dir_name" TEXT, "base_name" TEXT NOT NULL, "format_name" TEXT NOT NULL, "dst_table" TEXT NOT NULL, size INTEGER, mtime INTEGER);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html1' (Firewall TEXT, License TEXT, "Cost_and_usage_limits" TEXT, OS TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html2' (Firewall TEXT, License TEXT, Cost TEXT, OS TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html3' ("Can_Target" TEXT, "Changing_default_policy_to_accept_reject_by_issuing_a_single_rule" TEXT, "IP_destination_address_es" TEXT, "IP_source_address_es" TEXT, "TCP_UDP_destination_port_s" TEXT, "TCP_UDP_source_port_s" TEXT, "Ethernet_MAC_destination_address" TEXT, "Ethernet_MAC_source_address" TEXT, "Inbound_firewall_ingress" TEXT, "Outbound_firewall_egress" TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html4' (Can TEXT, "work_at_OSI_Layer_4_stateful_firewall" TEXT, "work_at_OSI_Layer_7_application_inspection" TEXT, "Change_TTL_Transparent_to_traceroute" TEXT, "Configure_REJECT_with_answer" TEXT, "DMZ_de_militarized_zone_allows_for_single_several_hosts_not_to_be_firewalled" TEXT, "Filter_according_to_time_of_day" TEXT, "Redirect_TCP_UDP_ports_port_forwarding" TEXT, "Redirect_IP_addresses_forwarding" TEXT, "Filter_according_to_User_Authorization" TEXT, "Traffic_rate_limit_QoS" TEXT, Tarpit TEXT, Log TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html5' (Features TEXT, "Configuration_GUI_text_or_both_modes" TEXT, "Remote_Access_Web_HTTP_Telnet_SSH_RDP_Serial_COM_RS232" TEXT, "Change_rules_without_requiring_restart" TEXT, "Ability_to_centrally_manage_all_firewalls_together" TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html6' (Features TEXT, "Modularity_supports_third_party_modules_to_extend_functionality" TEXT, "IPS _Intrusion_prevention_system" TEXT, "Open_Source_License" TEXT, "supports_IPv6" TEXT, "Class_Home_Professional" TEXT, "Operating_Systems_on_which_it_runs" TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html7' (Can TEXT, "NAT44_static_dynamic_w_o_ports_PAT" TEXT, "NAT64_NPTv6" TEXT, "IDS_Intrusion_Detection_System" TEXT, "VPN_Virtual_Private_Network" TEXT, "AV_Anti_Virus" TEXT, Sniffer TEXT, "Profile_selection" TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html8' ("vteFirewall_software" TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html9' (A TEXT, B TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html10' (A TEXT, B TEXT);
        CREATE TABLE IF NOT EXISTS 'Comparison_of_firewalls_Wikipedia_html11' (A TEXT, B TEXT);

For more information
~~~~~~~~~~~~~~~~~~~~~~
More examples are available at 
https://sqlitebiter.rtfd.io/en/latest/pages/usage/index.html

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
      completion  A helper command to setup command completion.
      configure   Configure the following application settings: (1) Default...
      file        Convert tabular data within CSV/Excel/HTML/JSON/Jupyter...
      gs          Convert a spreadsheet in Google Sheets to a SQLite database...
      url         Scrape tabular data from a URL and convert data to a SQLite...


Installation for macOS via Homebrew
----------------------------------------------------------

.. code:: console

    $ brew tap thombashi/sqlitebiter
    $ brew install sqlitebiter

- `Homebrew Formula <https://github.com/thombashi/homebrew-sqlitebiter>`__


Command Completion
----------------------------------------------------------
.. code:: console

    To setup for bash:

        sqlitebiter completion bash >> ~/.bashrc

    To setup for zsh:

        sqlitebiter completion zsh >> ~/.zshrc


Dependencies
============
Python 2.7+ or 3.4+

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
Extra Python packages are required to install to use Google Sheets feature:

- `gspread <https://github.com/burnash/gspread>`_
- `oauth2client <https://github.com/google/oauth2client/>`_
- `pyOpenSSL <https://pyopenssl.readthedocs.io/en/stable/>`_

The above packages can be installed with the following pip command;

.. code:: console

    $ pip install sqlitebiter[gs]

Test dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

Documentation
===============
https://sqlitebiter.rtfd.io/

