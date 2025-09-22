from domain.token import Operator


class Add(Operator):
    _symbol = '+'

    def execute(self, a: float, b: float) -> float:
        return a + b


class Subtract(Operator):
    _symbol = '-'

    def execute(self, a: float, b: float) -> float:
        return b - a


class Multiply(Operator):
    _symbol = '*'

    def execute(self, a: float, b: float) -> float:
        return a * b


class Divide(Operator):
    _symbol = '/'

    def execute(self, a: float, b: float) -> float:
        if a == 0:
            raise ValueError('Division by zero')
        return b / a
