from typing import List

from domain.token import Token


class ShutingYard:
    """Алгоритм сортировочной станции для преобразования инфиксной записис в обратную польскую последовательность"""

    def convert(self, tokens: List[Token]) -> List[Token]:
        return []


class RPNConverter:
    """Конвертер - заглушка для уже обратной польской записи"""

    def convert(self, tokens: List[Token]) -> List[Token]:
        return tokens
