# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import pytest
from sqlitebiter._ipynb_converter import is_ipynb_file_path, is_ipynb_url


class Test_is_ipynb_file_path(object):
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["test.ipynb", True],
            ["test.html", False],
            ["test", False],
            ["https://pypi.org/", False],
            ["https://pypi.org", False],
            ["", False],
            [
                "https://raw.githubusercontent.com/thombashi/pytablewriter/master/examples/ipynb/pytablewriter_examples.ipynb",
                False,
            ],
        ],
    )
    def test_normal(self, value, expected):
        assert is_ipynb_file_path(value) == expected


class Test_is_ipynb_url(object):
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["test.ipynb", False],
            ["test.html", False],
            ["test", False],
            ["https://pypi.org/", False],
            ["https://pypi.org", False],
            ["", False],
            [
                "https://raw.githubusercontent.com/thombashi/pytablewriter/master/examples/ipynb/pytablewriter_examples.ipynb",
                True,
            ],
        ],
    )
    def test_normal(self, value, expected):
        assert is_ipynb_url(value) == expected
