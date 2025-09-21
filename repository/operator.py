from typing import Dict

from domain.exception import InvalidTokenError
from domain.operator import (
    Add,
    Divide,
    Multiply,
    Subtract,
)
from domain.token import Operator


class OperatorRepository:
    """Репозиторий операторов"""

    _operators: Dict[str, Operator] = {
        '+': Add(),
        '-': Subtract(),
        '*': Multiply(),
        '/': Divide(),
    }

    def get_operator(self, symbol: str) -> Operator:
        """Возвращает оператор по символу"""
        if symbol not in self._operators:
            raise InvalidTokenError(f'Unknown operator: {symbol}')
        return self._operators[symbol]

    def is_operator(self, symbol: str) -> bool:
        """Проверяет, является ли символ оператором"""
        return symbol in self._operators
