import pytest

from domain.operator import Add, Subtract
from domain.token import Number
from domain.unary import UnaryMinus
from repository.rpn_calculator import RPNCalculator


@pytest.fixture
def calc() -> RPNCalculator:
    return RPNCalculator()


@pytest.mark.parametrize(
    'expr,expected',
    [
        ((Number(2), Number(2), Add()), 4),
        ((Number(2), Number(2), UnaryMinus(), Add()), 0),
        ((Number(2), Number(2), UnaryMinus(), Subtract()), 4),
    ],
)
def test_rpn_calculator(calc: RPNCalculator, expr, expected):
    assert calc.calculate(expr) == expected
