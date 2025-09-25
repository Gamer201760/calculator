from typing import List

from domain.exception import InvalidExpressionError
from domain.token import LParen, RParen, Token


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
