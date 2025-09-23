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


class Pow(Operator):
    _symbol = '^'

    def execute(self, a: float, b: float) -> float:
        return b**a


class IntegerDivide(Operator):
    _symbol = '//'

    def execute(self, a: float, b: float) -> float:
        if a == 0:
            raise ValueError('Division by zero')

        # Проверяем, что оба числа целые
        if not (a.is_integer() and b.is_integer()):
            raise TypeError('Integer division requires integer operands')

        return float(int(b) // int(a))


class Modulo(Operator):
    _symbol = '%'

    def execute(self, a: float, b: float) -> float:
        if a == 0:
            raise ValueError('Modulo by zero')

        # Проверяем, что оба числа целые
        if not (a.is_integer() and b.is_integer()):
            raise TypeError('Modulo operation requires integer operands')

        return float(int(b) % int(a))
