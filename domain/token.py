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
    @abstractmethod
    def execute(self, a: float, b: float) -> float: ...

    @abstractmethod
    def symbol(self) -> str: ...
