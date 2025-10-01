from domain.token import UnaryOperator


class UnaryMinus(UnaryOperator):
    _symbol = '~'
    _left_associativity = True
    _precedence = 3

    def execute(self, a: float) -> float:
        return (-1) * a


class UnaryPlus(UnaryOperator):
    _symbol = '$'
    _left_associativity = True
    _precedence = 3

    def execute(self, a: float) -> float:
        return (1) * a
