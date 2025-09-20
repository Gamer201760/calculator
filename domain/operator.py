from typing import Protocol


class Operator(Protocol):
    def execute(self, a: float, b: float) -> float: ...

    def symbol(self) -> str: ...


class AddOperator:
    def execute(self, a: float, b: float) -> float:
        return a + b

    def symbol(self) -> str:
        return "+"


class SubtractOperator:
    def execute(self, a: float, b: float) -> float:
        return a - b

    def symbol(self) -> str:
        return "-"


class MultiplyOperator:
    def execute(self, a: float, b: float) -> float:
        return a * b

    def symbol(self) -> str:
        return "*"


class DivideOperator:
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero")
        return a / b

    def symbol(self) -> str:
        return "/"
