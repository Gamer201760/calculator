from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol


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
        """Проверяет подклассы на наличе атрибутов и их типы"""
        super().__init_subclass__(**kwargs)
        required = {
            '_symbol': str,
            '_precedence': int,
            '_left_associativity': bool,
        }
        for name, expected_type in required.items():
            if not hasattr(cls, name):  # Проверям наличие атрибута у подкласса
                raise TypeError(f"Class '{cls.__name__}' must define '{name}'")
            value = getattr(cls, name)  # Получаем атрибут
            if not isinstance(value, expected_type):  # Проверяем тип атрибута
                raise TypeError(
                    f"Attribute '{name}' in '{cls.__name__}' must be '{expected_type.__name__}', \
                    got '{type(value).__name__}'"
                )


class UnaryOperator(Token, ABC):
    """Интерфейс токена для унарных операторов"""

    _symbol: str
    _precedence: int
    _left_associativity: bool

    @abstractmethod
    def execute(self, a: float) -> float: ...

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
        """Проверяет подклассы на наличе атрибутов и их типы"""
        super().__init_subclass__(**kwargs)
        required = {
            '_symbol': str,
        }
        for name, expected_type in required.items():
            if not hasattr(cls, name):  # Проверям наличие атрибута у подкласса
                raise TypeError(f"Class '{cls.__name__}' must define '{name}'")
            value = getattr(cls, name)  # Получаем атрибут
            if not isinstance(value, expected_type):  # Проверяем тип атрибута
                raise TypeError(
                    f"Attribute '{name}' in '{cls.__name__}' must be '{expected_type.__name__}', \
                    got '{type(value).__name__}'"
                )


class OperatorInterface(Protocol):
    """
    Интерфейс для всех операторов,
    который определяет такие геттеры как: symbol, precedence, associativity
    для сравнения приоритетов бинарных и унарных операторов
    """

    @property
    def symbol(self) -> str: ...

    @property
    def precedence(self) -> int: ...

    @property
    def left_associativity(self) -> bool: ...
