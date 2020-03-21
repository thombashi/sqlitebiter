Installation
============

Installation: pip (Python package manager)
----------------------------------------------------------
::

    pip install sqlitebiter


Installation: apt
----------------------------------------------------------------------------
You can install the package by ``apt`` via a Personal Package Archive (`PPA <https://launchpad.net/~thombashi/+archive/ubuntu/ppa>`__):

::

    sudo add-apt-repository ppa:thombashi/ppa
    sudo apt update
    sudo apt install sqlitebiter


Installation: dpkg (``.deb`` package)
----------------------------------------------------------------------------
The following commands will download the latest ``.deb`` package from the `release page <https://github.com/thombashi/sqlitebiter/releases>`__, and install it.

::

    curl -sSL https://raw.githubusercontent.com/thombashi/sqlitebiter/master/scripts/installer.sh | sudo bash


Installation: Windows
----------------------------------------------------------
``sqlitebiter`` can be used in Windows environments without Python installation as follows:

#. Navigate to https://github.com/thombashi/sqlitebiter/releases
#. Download the latest version of the ``sqlitebiter_win_x64.zip``
#. Unzip the file
#. Execute ``sqlitebiter.exe`` in either Command Prompt or PowerShell


Installation: Windows (PowerShell)
----------------------------------------------------------
The following commands will download the latest execution binary from the `release page <https://github.com/thombashi/sqlitebiter/releases>`__ to the current directory.

::

    wget https://github.com/thombashi/sqlitebiter/raw/master/scripts/get-sqlitebiter.ps1 -OutFile get-sqlitebiter.ps1
    Set-ExecutionPolicy Unrestricted -Scope Process -Force; .\get-sqlitebiter.ps1


Installation: brew for macOS
----------------------------------------------------------
.. code:: console

    $ brew tap thombashi/sqlitebiter
    $ brew install sqlitebiter

- `Homebrew Formula <https://github.com/thombashi/homebrew-sqlitebiter>`__


Command Completion (bash/zsh)
----------------------------------------------------------
.. code:: console

    setup command completion for bash:

        sqlitebiter completion bash >> ~/.bashrc

    setup command completion for zsh:

        sqlitebiter completion zsh >> ~/.zshrc


Dependencies
============
Python 3.5+

Python package dependencies
------------------------------------------------------------

Mandatory dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Following mandatory Python packages are automatically installed during
``sqlitebiter`` installation process:

- `appconfigpy <https://github.com/thombashi/appconfigpy>`__
- `click <https://palletsprojects.com/p/click/>`__
- `colorama <https://github.com/tartley/colorama>`__
- `loguru <https://github.com/Delgan/loguru>`__
- `msgfy <https://github.com/thombashi/msgfy>`__
- `nbformat <https://jupyter.org/>`__
- `path <https://github.com/jaraco/path>`__
- `pathvalidate <https://github.com/thombashi/pathvalidate>`__
- `pytablereader <https://github.com/thombashi/pytablereader>`__
- `retryrequests <https://github.com/thombashi/retryrequests>`__
- `SimpleSQLite <https://github.com/thombashi/SimpleSQLite>`__
- `typepy <https://github.com/thombashi/typepy>`__

Google Sheets dependencies (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Extra Python packages are required to install to use Google Sheets feature (`gs` subcommand):

- `gspread <https://github.com/burnash/gspread>`_
- `oauth2client <https://github.com/google/oauth2client/>`_
- `pyOpenSSL <https://pyopenssl.readthedocs.io/en/stable/>`_

The extra packages can be installed with the following `pip` command;

.. code:: console

    $ pip install sqlitebiter[gs]

note: binary packages include these dependencies

Test dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- `pytest <https://docs.pytest.org/en/latest/>`__
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
