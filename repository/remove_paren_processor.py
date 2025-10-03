from typing import List

from domain.token import LParen, RParen, Token


class RemoveParenProcessor:
    """Удаляет скобки, для rpn"""

    def process(self, tokens: List[Token]) -> List[Token]:
        return [token for token in tokens if not isinstance(token, (LParen, RParen))]
