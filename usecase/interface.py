from typing import List, Protocol

from domain.token import Operator, Token


class TokenParserInterface(Protocol):
    """Интерфейс для парсера токенов"""

    def parse(self, expression: str) -> List[Token]:
        """Парсит строку в список токенов"""
        ...


class OperatorRepositoryInterface(Protocol):
    """Интерфейс для репозитория операторов"""

    def get_operator(self, symbol: str) -> Operator:
        """Возвращает оператор по символу"""
        ...

    def is_operator(self, symbol: str) -> bool:
        """Проверяет, является ли символ оператором"""
        ...
