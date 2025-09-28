from typing import List

from domain.exception import InsufficientOperandsError, InvalidExpressionError
from domain.token import Number, Operator, Token, UnaryOperator


class RPNCalculator:
    def calculate(self, tokens: List[Token]) -> float:
        """Вычисляет список токенов используя стек"""
        stack: List[float] = []

        for token in tokens:
            if isinstance(token, Number):
                stack.append(token.value)
            elif isinstance(token, Operator):
                if len(stack) < 2:
                    raise InsufficientOperandsError(
                        f"Insufficient operands for operator '{token.symbol}'"
                    )

                result = token.execute(stack.pop(), stack.pop())
                stack.append(result)
            elif isinstance(token, UnaryOperator):
                if not stack:
                    raise InsufficientOperandsError(
                        f"Insufficient operand for unary operator '{token.symbol}'"
                    )
                result = token.execute(stack.pop())
                stack.append(result)

        if len(stack) != 1:
            raise InvalidExpressionError(
                'Invalid RPN expression: incorrect number of operands'
            )

        return stack[0]
