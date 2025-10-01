from domain.error import CalculationError
from domain.token import Operator


class Add(Operator):
    _symbol = '+'
    _precedence = 1
    _left_associativity = True

    def execute(self, a: float, b: float) -> float:
        return a + b


class Subtract(Operator):
    _symbol = '-'
    _precedence = 1
    _left_associativity = True

    def execute(self, a: float, b: float) -> float:
        return b - a


class Multiply(Operator):
    _symbol = '*'
    _precedence = 2
    _left_associativity = True

    def execute(self, a: float, b: float) -> float:
        return a * b


class Divide(Operator):
    _symbol = '/'
    _precedence = 2
    _left_associativity = True

    def execute(self, a: float, b: float) -> float:
        if a == 0:
            raise CalculationError('Деление на ноль')
        return b / a


class Pow(Operator):
    _symbol = '^'
    _precedence = 4
    _left_associativity = False

    def execute(self, a: float, b: float) -> float:
        return b**a


class IntegerDivide(Operator):
    _symbol = '//'
    _precedence = 2
    _left_associativity = True

    def execute(self, a: float, b: float) -> float:
        if a == 0:
            raise CalculationError('Деление на ноль')

        if not (a.is_integer() and b.is_integer()):
            raise CalculationError(
                'Для целочисленного деления требуются целые операнды'
            )

        return float(int(b) // int(a))


class Modulo(Operator):
    _symbol = '%'
    _precedence = 2
    _left_associativity = True

    def execute(self, a: float, b: float) -> float:
        if a == 0:
            raise CalculationError('Деление на ноль')

        if not (a.is_integer() and b.is_integer()):
            raise CalculationError(
                'Для операции взятия остатка требуются целые операнды'
            )

        return float(int(b) % int(a))
