from domain.token import UnaryOperator


class UnaryMinus(UnaryOperator):
    _symbol = '~'

    def execute(self, a: float) -> float:
        return (-1) * a


class UnaryPlus(UnaryOperator):
    _symbol = '$'

    def execute(self, a: float) -> float:
        return (1) * a
