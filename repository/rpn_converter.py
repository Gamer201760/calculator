from typing import List

from domain.token import Token


class RPNConverter:
    """
    Конвертер - заглушка для уже обратной польской записи
    """

    def convert(self, tokens: List[Token]) -> List[Token]:
        return tokens
