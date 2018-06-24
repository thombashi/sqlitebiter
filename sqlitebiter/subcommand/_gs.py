# encoding: utf-8

'''
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
'''

from __future__ import absolute_import, unicode_literals

import msgfy
import pytablereader as ptr
import simplesqlite as sql
import six

from .._common import get_success_message
from ._base import TableConverter


class GoogleSheetsConverter(TableConverter):

    def convert(self, credentials, title):
        logger = self._logger
        verbosity_level = self._verbosity_level
        result_counter = self._result_counter

        loader = ptr.GoogleSheetsTableLoader()
        loader.source = credentials
        loader.title = title

        # if typepy.is_null_string(loader.source):
        #     loader.source = app_config_manager.load().get(
        #         ConfigKey.GS_CREDENTIALS_FILE_PATH)

        try:
            for table_data in loader.load():
                logger.debug(u"loaded table_data: {}".format(six.text_type(table_data)))

                sqlite_tabledata = sql.SQLiteTableDataSanitizer(table_data).normalize()

                try:
                    self._table_creator.create(sqlite_tabledata, self._index_list)
                    result_counter.inc_success()
                except (ptr.ValidationError, ptr.DataError):
                    result_counter.inc_fail()

                logger.info(get_success_message(
                    verbosity_level, "google sheets",
                    self._schema_extractor.get_table_schema_text(sqlite_tabledata.table_name)))
        except ptr.OpenError as e:
            logger.error(msgfy.to_error_message(e))
            result_counter.inc_fail()
        except (ptr.ValidationError, ptr.DataError) as e:
            logger.error(u"invalid credentials data: path={}, message={}".format(
                credentials, str(e)))
            result_counter.inc_fail()
        except ptr.APIError as e:
            logger.error(msgfy.to_error_message(e))
            result_counter.inc_fail()
