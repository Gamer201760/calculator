from typing import List, Protocol

from domain.token import Token


class TokenizerInterface(Protocol):
    """Интерфейс для парсера токенов"""

    def parse(self, expression: str) -> List[Token]:
        """Парсит строку в список токенов"""
        ...


class RPNConverterInterface(Protocol):
    """Интерфейс для преобразования списка токенов в обратную польскую последовательность"""

    def convert(self, tokens: List[Token]) -> List[Token]: ...


class ValidatorInterface(Protocol):
    """Интерфейс валидатора выражений"""

    def validate(self, tokens: List[Token]) -> None:
        """Валидирует список токенов, выбрасывает исключение при ошибке"""
        ...
