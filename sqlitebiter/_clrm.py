# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import sys

from colorama import Fore, Style


def _wrap_color(text, color):
    return "{}{}{}".format(color, text, Fore.RESET)


def _wrap_style(text, style):
    return "{}{}{}".format(style, text, Style.RESET_ALL)


def red(text):
    return _wrap_color(text, Fore.RED)


def green(text):
    return _wrap_color(text, Fore.GREEN)


def yellow(text):
    return _wrap_color(text, Fore.YELLOW)


def cyan(text):
    return _wrap_color(text, Fore.CYAN)


def white(text):
    return _wrap_color(text, Fore.WHITE)


def bright(text):
    return _wrap_style(text, Style.BRIGHT)
