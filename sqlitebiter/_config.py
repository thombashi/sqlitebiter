#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import appconfigpy

from ._const import PROGRAM_NAME


class ConfigKey(object):
    PROXY_SERVER = "proxy_server"
    GS_CREDENTIALS_FILE_PATH = "gs_credentials_file_path"


app_config_manager = appconfigpy.ConfigManager(
    config_name=PROGRAM_NAME,
    config_item_list=[
        appconfigpy.ConfigItem(
            name=ConfigKey.PROXY_SERVER,
            prompt_text="HTTP/HTTPS proxy server URI",
            initial_value="",
        ),
        # appconfigpy.ConfigItem(
        #    name="gs_credentials_file_path",
        #    prompt_text="Google Sheets credentials file path",
        #    initial_value="",
        # ),
    ])
