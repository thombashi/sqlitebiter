``sqlitebiter`` command help
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``sqlitebiter`` has following subcommands:

- ``file``: Convert tabular data within CSV/Excel/HTML/JSON/LTSV/Markdown/SQLite/TSV file(s) to a SQLite database file.
    - :doc:`file/index`
- ``url``: Scrape tabular data from a URL and convert data to a SQLite database file.
    - :doc:`url/index`
- ``gs``: Convert a spreadsheet in Google Sheets to a SQLite database file.
    - :doc:`gs/index`
- ``configure``: Configure the application settings

::

    Usage: sqlitebiter [OPTIONS] COMMAND [ARGS]...

    Options:
      --version      Show the version and exit.
      --append       append table(s) to existing database.
      -v, --verbose
      --debug        for debug print.
      --quiet        suppress execution log messages.
      -h, --help     Show this message and exit.

    Commands:
      configure  Configure the following application settings:...
      file       Convert tabular data within...
      gs         Convert a spreadsheet in Google Sheets to a...
      url        Scrape tabular data from a URL and convert...
