from domain.token import Operator


class AddOperator(Operator):
    def execute(self, a: float, b: float) -> float:
        return a + b

    def symbol(self) -> str:
        return '+'


class SubtractOperator(Operator):
    def execute(self, a: float, b: float) -> float:
        return a - b

    def symbol(self) -> str:
        return '-'


class MultiplyOperator(Operator):
    def execute(self, a: float, b: float) -> float:
        return a * b

    def symbol(self) -> str:
        return '*'


class DivideOperator(Operator):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError('Division by zero')
        return a / b

    def symbol(self) -> str:
        return '/'
