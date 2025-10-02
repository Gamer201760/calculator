import pytest

from domain.error import InvalidExpressionError
from domain.operator import Add, Pow, Subtract
from domain.token import LParen, Number, RParen
from domain.unary import UnaryMinus
from repository.validator import OperatorSequenceValidator
from usecase.interface import ValidatorInterface


@pytest.fixture
def validator() -> ValidatorInterface:
    return OperatorSequenceValidator()


@pytest.mark.parametrize(
    'expr',
    [
        ([Number(1), Add(), Number(2)]),
        ([LParen(), Number(1), Pow(), Number(2), RParen()]),
        ([Number(1), Subtract(), LParen(), UnaryMinus(), Number(1), RParen()]),
    ],
)
def test_valid(validator: ValidatorInterface, expr):
    validator.validate(expr)


@pytest.mark.parametrize(
    'expr',
    [
        ([Add(), Add(), Pow()]),
        ([Number(3), Subtract(), UnaryMinus(), Number(1)]),
        ([Subtract(), UnaryMinus(), Number(1), RParen()]),
    ],
)
def test_invalid(validator: ValidatorInterface, expr):
    with pytest.raises(InvalidExpressionError):
        validator.validate(expr)
