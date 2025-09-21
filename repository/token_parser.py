from typing import List

from domain.exception import InvalidTokenError
from domain.token import Number, Token
from usecase.interface import OperatorRepositoryInterface, TokenParserInterface


class TokenParser(TokenParserInterface):
    """Парсер токенов из строки"""

    def __init__(self, operator_repository: OperatorRepositoryInterface):
        self._operator_repository = operator_repository

    def parse(self, expression: str) -> List[Token]:
        """Парсит строку в список токенов"""
        tokens: List[Token] = []
        elements = expression.split()

        for element in elements:
            if self._is_number(element):
                tokens.append(Number(float(element)))
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
