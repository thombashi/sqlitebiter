"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from ._const import ExitCode


class ResultCounter:
    @property
    def success_count(self) -> int:
        return self.__success_count

    @property
    def fail_count(self) -> int:
        return self.__fail_count

    @property
    def skip_count(self) -> int:
        return self.__skip_count

    @property
    def total_count(self) -> int:
        return self.success_count + self.fail_count + self.skip_count

    @property
    def created_table_count(self) -> int:
        return self.__create_table_count

    def __init__(self) -> None:
        self.__create_table_count = 0
        self.__success_count = 0
        self.__fail_count = 0
        self.__skip_count = 0

    def __repr__(self) -> str:
        return "results: " + ", ".join(
            [
                f"success={self.__success_count:d}",
                f"failed={self.__fail_count:d}",
                f"skip={self.__skip_count:s}",
                f"return_code={self.get_return_code():d}",
            ]
        )

    def inc_success(self, is_create_table: bool) -> None:
        self.__success_count += 1

        if is_create_table:
            self.__create_table_count += 1

    def inc_fail(self) -> None:
        self.__fail_count += 1

    def inc_skip(self) -> None:
        self.__skip_count += 1

    def get_return_code(self) -> int:
        if self.__success_count > 0:
            return ExitCode.SUCCESS

        if self.__fail_count > 0:
            return ExitCode.FAILED_CONVERT

        return ExitCode.NO_INPUT
