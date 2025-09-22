from domain.token import Operator


class Add(Operator):
    def execute(self, a: float, b: float) -> float:
        return a + b

    def symbol(self) -> str:
        return '+'


class Subtract(Operator):
    def execute(self, a: float, b: float) -> float:
        return b - a

    def symbol(self) -> str:
        return '-'


class Multiply(Operator):
    def execute(self, a: float, b: float) -> float:
        return a * b

    def symbol(self) -> str:
        return '*'


class Divide(Operator):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError('Division by zero')
        return b / a

    def symbol(self) -> str:
        return '/'
