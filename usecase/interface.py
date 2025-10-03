from typing import List, Protocol

from domain.token import Token


class TokenizerInterface(Protocol):
    """Интерфейс для парсера токенов"""

    def parse(self, expression: str) -> List[Token]: ...


class RPNConverterInterface(Protocol):
    """Интерфейс для преобразования списка токенов в обратную польскую последовательность"""

    def convert(self, tokens: List[Token]) -> List[Token]: ...


class ValidatorInterface(Protocol):
    """
    Интерфейс валидатора выражений,
    валидирует список токенов,
    выбрасывает исключение при ошибке
    """

    def validate(self, tokens: List[Token]) -> None: ...


class ProcessorInterface(Protocol):
    """
    Интерфейс процессора для токенов,
    запускается после токенизатора,
    для преобразования токенов
    """

    def process(self, tokens: List[Token]) -> List[Token]: ...
