"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import click
import msgfy
import pytablereader as ptr

from ._base import SourceInfo, TableConverter


class GoogleSheetsConverter(TableConverter):
    def convert(self, credentials: click.Path, title: str) -> None:
        logger = self._logger
        result_counter = self._result_counter
        source_id = self._fetch_next_source_id()

        loader = ptr.GoogleSheetsTableLoader()
        loader.source = credentials
        loader.title = title

        # if typepy.is_null_string(loader.source):
        #     loader.source = app_config_mgr.load().get(
        #         ConfigKey.GS_CREDENTIALS_FILE_PATH)

        try:
            for table_data in loader.load():
                logger.debug(f"loaded table_data: {str(table_data)}")

                sqlite_tabledata = self.normalize_table(table_data)
                source_info = SourceInfo(
                    base_name=title,
                    dst_table=sqlite_tabledata.table_name,
                    format_name=self._format_name,
                    source_id=source_id,
                )

                try:
                    self._table_creator.create(
                        sqlite_tabledata, self._index_list, source_info=source_info
                    )
                    SourceInfo.insert(source_info)
                except (ptr.ValidationError, ptr.DataError):
                    result_counter.inc_fail()
        except ptr.OpenError as e:
            logger.error(msgfy.to_error_message(e))
            result_counter.inc_fail()
        except (ptr.ValidationError, ptr.DataError) as e:
            logger.error(f"invalid credentials data: path={credentials}, message={str(e)}")
            result_counter.inc_fail()
        except ptr.APIError as e:
            logger.error(msgfy.to_error_message(e))
            result_counter.inc_fail()
        except ImportError as e:
            logger.error(
                "{}: try to install dependencies with 'pip install sqlitebiter[gs]'".format(
                    msgfy.to_error_message(e)
                )
            )
        except OverflowError as e:
            logger.error(f"{title}: {e}")
            result_counter.inc_fail()
