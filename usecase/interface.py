from abc import ABC, abstractmethod
from typing import List

from domain.token import Operator, Token


class TokenParserInterface(ABC):
    """Интерфейс для парсера токенов"""

    @abstractmethod
    def parse(self, expression: str) -> List[Token]:
        """Парсит строку в список токенов"""
        ...


class OperatorRepositoryInterface(ABC):
    """Интерфейс для репозитория операторов"""

    @abstractmethod
    def get_operator(self, symbol: str) -> Operator:
        """Возвращает оператор по символу"""
        ...

    @abstractmethod
    def is_operator(self, symbol: str) -> bool:
        """Проверяет, является ли символ оператором"""
        ...
