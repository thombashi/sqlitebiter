``sqlitebiter`` command help
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``sqlitebiter`` has three subcommands:

- ``file``: Convert tabular data within CSV/Excel/HTML/JSON/LTSV/Markdown/TSV file(s) to a SQLite database file.
    - :doc:`file/index`
- ``url``: Scrape tabular data from a URL and convert data to a SQLite database file.
    - :doc:`url/index`
- ``gs``: Convert a spreadsheet in Google Sheets to a SQLite database file.
    - :doc:`gs/index`

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
      file  Convert tabular data within...
      gs    Convert Google Sheets to a SQLite database...
      url   Fetch data from a URL and convert data to a...
