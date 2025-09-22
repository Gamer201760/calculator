from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Token(ABC):
    """Базовый класс для всех токенов в RPN выражении"""

    ...


@dataclass
class Number(Token):
    value: float


class LeftParen(Token):
    """Левая скобка"""


class RightParen(Token):
    """Правая скобка"""


class Operator(Token, ABC):
    _symbol: str

    @abstractmethod
    def execute(self, a: float, b: float) -> float: ...

    def get_symbol(self) -> str:
        return self._symbol

    def __hash__(self) -> int:
        return hash(self._symbol)
