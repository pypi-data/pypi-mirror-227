from collections import Counter
from functools import lru_cache


class LetterCounter:
    """Find unique letters"""

    @lru_cache
    def _count_unique_letters(self, string: str) -> int:
        """Find unique letters which appear only once

        :return: amount of letters
        """
        if isinstance(string, str) and string.isascii():
            return list(Counter(string).values()).count(1)

    def count(self, any_data: str) -> int:
        """Function validate for a correct data which transmits into previous functions

        :return: amount of letters
        """
        if isinstance(any_data, str):
            return LetterCounter()._count_unique_letters(any_data)
