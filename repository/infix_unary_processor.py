from itertools import pairwise
from typing import List

from domain.operator import Add, Subtract
from domain.token import LParen, Number, Operator, Token
from domain.unary import UnaryMinus, UnaryPlus


class InfixUnaryProcessor:
    """
    Преобразует базовые токены, заменяя бинарные '+' и '-'
    на унарные
    """

    def process(self, tokens: List[Token]) -> List[Token]:
        processed_tokens: List[Token] = []

        for curr, next in pairwise(tokens):
            prev = processed_tokens[-1] if len(processed_tokens) > 0 else None
            if isinstance(next, (Number, LParen)) and (
                prev is None or isinstance(prev, (Operator, LParen))
            ):
                if isinstance(curr, Subtract):
                    processed_tokens.append(UnaryMinus())
                elif isinstance(curr, Add):
                    processed_tokens.append(UnaryPlus())
                else:
                    processed_tokens.append(curr)  # TODO: refactor
            else:
                processed_tokens.append(curr)
        processed_tokens.append(next)

        return processed_tokens
