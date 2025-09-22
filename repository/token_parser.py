from typing import List, Protocol

from domain.exception import InvalidTokenError
from domain.token import LParen, Number, Operator, RParen, Token


class OperatorRepositoryInterface(Protocol):
    """Интерфейс для репозитория операторов"""

    def get_operator(self, symbol: str) -> Operator:
        """Возвращает оператор по символу"""
        ...

    def is_operator(self, symbol: str) -> bool:
        """Проверяет, является ли символ оператором"""
        ...


class SpaceTokenizer:
    """Парсер токенов из строки строго по пробелам"""

    def __init__(self, operator_repository: OperatorRepositoryInterface):
        self._operator_repository = operator_repository

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
            elif self._operator_repository.is_operator(element):
                operator = self._operator_repository.get_operator(element)
                tokens.append(operator)
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
