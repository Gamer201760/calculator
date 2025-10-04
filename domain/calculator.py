from typing import List

from domain.error import CalculationError
from domain.token import Number, Operator, Token, UnaryOperator


class RPNCalculator:
    """
    Вычисляет список токенов в обратной польской нотации, используя стек
    Ожидает валидное выражение
    """

    def calculate(self, tokens: List[Token]) -> float:
        stack: List[float] = []

        try:
            for token in tokens:
                if isinstance(token, Number):
                    stack.append(token.value)
                elif isinstance(token, Operator):
                    result = token.execute(stack.pop(), stack.pop())
                    stack.append(result)
                elif isinstance(token, UnaryOperator):
                    result = token.execute(stack.pop())
                    stack.append(result)
        except OverflowError:
            raise CalculationError('Результат вычисления слишком велик')
        return stack[0]
