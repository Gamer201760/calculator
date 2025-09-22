from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Token(ABC):
    """Базовый класс для всех токенов в RPN выражении"""


@dataclass
class Number(Token):
    """Токен числа"""

    value: float


class LParen(Token):
    """Токен левой скобки"""


class RParen(Token):
    """Токен правой скобки"""


class Operator(Token, ABC):
    """Интерфейс токена для бинарных операторов"""

    _symbol: str

    @abstractmethod
    def execute(self, a: float, b: float) -> float: ...

    def get_symbol(self) -> str:
        return self._symbol

    def __hash__(self) -> int:
        return hash(self._symbol)
