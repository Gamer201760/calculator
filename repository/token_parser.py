from typing import Dict, List, Type

from domain.exception import InvalidTokenError
from domain.operator import Add, Divide, IntegerDivide, Modulo, Multiply, Pow, Subtract
from domain.token import LParen, Number, Operator, RParen, Token


class SpaceTokenizer:
    """Парсер токенов из строки строго по пробелам"""

    def __init__(self) -> None:
        self._operators: Dict[str, Type[Operator]] = {
            '+': Add,
            '-': Subtract,
            '*': Multiply,
            '/': Divide,
            '^': Pow,
            '//': IntegerDivide,
            '%': Modulo,
        }

    def parse(self, expression: str) -> List[Token]:
        """Парсит строку в список токенов"""
        tokens: List[Token] = []
        elements = expression.split()

        for element in elements:
            if self._is_number(element):
                tokens.append(Number(float(element)))
            elif element == '(':
                tokens.append(LParen())
            elif element == ')':
                tokens.append(RParen())
            elif element in self._operators:
                operator = self._operators[element]
                tokens.append(operator())
            else:
                raise InvalidTokenError(f'Invalid token: {element}')

        return tokens

    # TODO: refactor
    def _is_number(self, value: str) -> bool:
        """Проверяет, является ли строка числом"""
        try:
            float(value)
            return True
        except ValueError:
            return False
