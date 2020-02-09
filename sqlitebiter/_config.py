"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""


from appconfigpy import ConfigItem, ConfigManager

from ._const import PROGRAM_NAME


class ConfigKey:
    DEFAULT_ENCODING = "default_encoding"
    PROXY_SERVER = "proxy_server"
    GS_CREDENTIALS_FILE_PATH = "gs_credentials_file_path"


app_config_mgr = ConfigManager(
    PROGRAM_NAME,
    [
        ConfigItem(
            name=ConfigKey.DEFAULT_ENCODING,
            prompt_text="Default encoding to load files",
            initial_value="utf-8",
        ),
        ConfigItem(
            name=ConfigKey.PROXY_SERVER, prompt_text="HTTP/HTTPS proxy server URI", initial_value=""
        ),
        # ConfigItem(
        #    name="gs_credentials_file_path",
        #    prompt_text="Google Sheets credentials file path",
        #    initial_value="",
        # ),
    ],
)
