from typing import List

from domain.exception import InsufficientOperandsError, InvalidExpressionError
from domain.token import Number, Operator, Token, UnaryOperator


class RPNCalculatorRepository:
    def calculate(self, tokens: List[Token]) -> float:
        """Вычисляет список токенов используя стек"""
        stack: List[float] = []

        for token in tokens:
            if isinstance(token, Number):
                stack.append(token.value)
            elif isinstance(token, Operator):
                if len(stack) < 2:
                    raise InsufficientOperandsError(
                        f'Недостаточно операндов для бинарного оператора "{token.symbol}"'
                    )

                result = token.execute(stack.pop(), stack.pop())
                stack.append(result)
            elif isinstance(token, UnaryOperator):
                if not stack:
                    raise InsufficientOperandsError(
                        f'Недостаточно операндов для унарного оператора "{token.symbol}"'
                    )

                result = token.execute(stack.pop())
                stack.append(result)

        if len(stack) != 1:
            raise InvalidExpressionError(
                'Некорректное выражение в скобках: в конце должно оставаться одно значение'
            )

        return stack[0]
