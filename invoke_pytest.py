"""
Unit tests at Windows environments required to invoke from py module,
because of multiprocessing:
http://py.readthedocs.io/en/latest/faq.html?highlight=cmdline#issues-with-py-test-multiprocess-and-setuptools
"""

import os
import sys

import py


if __name__ == "__main__":
    os.environ["PYTEST_MD_REPORT_COLOR"] = "text"
    sys.exit(py.test.cmdline.main(["-vv"]))
