"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from colorama import Fore, Style


def _wrap_color(text: str, color: str) -> str:
    return "{}{}{}".format(color, text, Fore.RESET)


def _wrap_style(text: str, style: str) -> str:
    return "{}{}{}".format(style, text, Style.RESET_ALL)


def red(text: str) -> str:
    return _wrap_color(text, Fore.RED)


def green(text: str) -> str:
    return _wrap_color(text, Fore.GREEN)


def yellow(text: str) -> str:
    return _wrap_color(text, Fore.YELLOW)


def cyan(text: str) -> str:
    return _wrap_color(text, Fore.CYAN)


def white(text: str) -> str:
    return _wrap_color(text, Fore.WHITE)


def bright(text: str) -> str:
    return _wrap_style(text, Style.BRIGHT)
