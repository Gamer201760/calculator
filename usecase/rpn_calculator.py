from typing import List

from domain.exception import InsufficientOperandsError, InvalidExpressionError
from domain.token import Number, Operator, Token
from usecase.interface import TokenParserInterface


class RPNCalculatorUseCase:
    """Use case для вычисления RPN выражений"""

    def __init__(self, token_parser: TokenParserInterface):
        self._token_parser = token_parser

    def calculate(self, expression: str) -> float:
        """Вычисляет RPN выражение"""
        if not expression.strip():
            raise InvalidExpressionError('Empty expression')

        tokens = self._token_parser.parse(expression)
        return self._evaluate_tokens(tokens)

    def _evaluate_tokens(self, tokens: List[Token]) -> float:
        """Вычисляет список токенов используя стек"""
        stack: List[float] = []

        for token in tokens:
            if isinstance(token, Number):
                stack.append(token.value)
            elif isinstance(token, Operator):
                if len(stack) < 2:
                    raise InsufficientOperandsError(
                        f'Insufficient operands for operator {token.symbol()}'
                    )

                result = token.execute(stack.pop(), stack.pop())
                stack.append(result)

        if len(stack) != 1:
            raise InvalidExpressionError(
                'Invalid RPN expression: incorrect number of operands'
            )

        return stack[0]
