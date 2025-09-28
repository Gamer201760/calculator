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
    _precedence: int
    _left_associativity: bool

    @abstractmethod
    def execute(self, a: float, b: float) -> float: ...

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def precedence(self) -> int:
        return self._precedence

    @property
    def left_associativity(self) -> bool:
        return self._left_associativity

    def __hash__(self) -> int:
        return hash(self._symbol)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        required = {
            '_symbol': str,
            '_precedence': int,
            '_left_associativity': bool,
        }
        for name, expected_type in required.items():
            if not hasattr(cls, name):
                raise TypeError(f"Class '{cls.__name__}' must define '{name}'")
            value = getattr(cls, name)
            if not isinstance(value, expected_type):
                raise TypeError(
                    f"Attribute '{name}' in '{cls.__name__}' must be '{expected_type.__name__}', \
                    got '{type(value).__name__}'"
                )


class UnaryOperator(Token, ABC):
    """Интерфейс токена для унарных операторов"""

    _symbol: str

    @abstractmethod
    def execute(self, a: float) -> float: ...

    @property
    def symbol(self) -> str:
        return self._symbol

    def __hash__(self) -> int:
        return hash(self._symbol)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        required = {
            '_symbol': str,
        }
        for name, expected_type in required.items():
            if not hasattr(cls, name):
                raise TypeError(f"Class '{cls.__name__}' must define '{name}'")
            value = getattr(cls, name)
            if not isinstance(value, expected_type):
                raise TypeError(
                    f"Attribute '{name}' in '{cls.__name__}' must be '{expected_type.__name__}', \
                    got '{type(value).__name__}'"
                )
