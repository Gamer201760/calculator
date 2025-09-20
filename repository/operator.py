from typing import Dict

from domain.exception import InvalidTokenError
from domain.operator import (
    AddOperator,
    DivideOperator,
    MultiplyOperator,
    SubtractOperator,
)
from domain.token import Operator
from usecase.interface import OperatorRepositoryInterface


class OperatorRepository(OperatorRepositoryInterface):
    """Репозиторий операторов"""

    _operators: Dict[str, Operator] = {
        '+': AddOperator(),
        '-': SubtractOperator(),
        '*': MultiplyOperator(),
        '/': DivideOperator(),
    }

    def get_operator(self, symbol: str) -> Operator:
        """Возвращает оператор по символу"""
        if symbol not in self._operators:
            raise InvalidTokenError(f'Unknown operator: {symbol}')
        return self._operators[symbol]

    def is_operator(self, symbol: str) -> bool:
        """Проверяет, является ли символ оператором"""
        return symbol in self._operators
