import pytest

from domain.token import UnaryOperator
from domain.unary import UnaryMinus, UnaryPlus


@pytest.fixture
def minus() -> UnaryOperator:
    return UnaryMinus()


@pytest.fixture
def plus() -> UnaryOperator:
    return UnaryPlus()


@pytest.mark.parametrize(
    'expr,expected',
    [
        (2, -2),
        (-2, 2),
        ((2**2), -4),
        ((10 + 15 - 30), 5),
    ],
)
def test_unary_minus(minus: UnaryMinus, expr, expected):
    assert minus.execute(expr) == expected


@pytest.mark.parametrize(
    'expr,expected',
    [
        (-2, -2),
        (2, 2),
        ((2**2), 4),
        ((10 + 15 - 30), -5),
    ],
)
def test_unary_plus(plus: UnaryPlus, expr, expected):
    assert plus.execute(expr) == expected
