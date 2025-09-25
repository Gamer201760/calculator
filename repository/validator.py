from typing import List

from domain.exception import InvalidExpressionError
from domain.token import LParen, Operator, RParen, Token


class BalancedParenValidator:
    def validate(self, tokens: List[Token]) -> None:
        paren_count = 0
        for token in tokens:
            if isinstance(token, LParen):
                paren_count += 1
            elif isinstance(token, RParen):
                paren_count -= 1
                if paren_count < 0:
                    raise InvalidExpressionError('Unmatched closing parenthesis')

        if paren_count > 0:
            raise InvalidExpressionError('Unmatched opening parenthesis')


class OperatorPlacementValidator:
    """Проверяет последовательность операторов"""

    def validate(self, tokens: List[Token]) -> None:
        prev_token = None
        for i, token in enumerate(tokens):
            if isinstance(token, Operator):
                if i == 0 or i == len(tokens) - 1:
                    raise InvalidExpressionError(
                        f"Operator '{token.symbol}' at invalid position"
                    )

                if isinstance(prev_token, Operator):
                    raise InvalidExpressionError('Consecutive operators not allowed')

            prev_token = token
