from itertools import pairwise
from typing import List

from domain.operator import Add, Subtract
from domain.token import LParen, Number, Operator, Token
from domain.unary import UnaryMinus, UnaryPlus


class InfixUnaryProcessor:
    """
    Преобразует базовые токены,
    заменяя бинарные '+' и '-' на унарные
    """

    def process(self, tokens: List[Token]) -> List[Token]:
        processed_tokens: List[Token] = []

        for curr, next_token in pairwise(tokens):
            prev = processed_tokens[-1] if processed_tokens else None

            if self._should_convert_to_unary(curr, prev, next_token):
                processed_tokens.append(self._convert_to_unary(curr))
            else:
                processed_tokens.append(curr)

        processed_tokens.append(tokens[-1])
        return processed_tokens

    def _should_convert_to_unary(
        self, current: Token, prev: Token | None, next_token: Token
    ) -> bool:
        """Проверяет, нужно ли преобразовать оператор в унарный"""
        if not isinstance(current, (Add, Subtract)):
            return False

        # Следующий токен должен быть числом или открывающей скобкой
        if not isinstance(next_token, (Number, LParen)):
            return False

        # Предыдущий токен должен быть None, оператором или открывающей скобкой
        return prev is None or isinstance(prev, (Operator, LParen))

    def _convert_to_unary(self, token: Token) -> Token:
        """Преобразует бинарный оператор в унарный"""
        if isinstance(token, Subtract):
            return UnaryMinus()
        elif isinstance(token, Add):
            return UnaryPlus()
        return token
