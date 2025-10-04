import pytest

from domain.error import DomainError, InvalidExpressionError
from domain.operator import Add, Pow, Subtract
from domain.token import LParen, Number, RParen
from domain.unary import UnaryMinus
from repository.validator import ExpressionEmptyValidator
from usecase.interface import ValidatorInterface


@pytest.fixture
def validator() -> ValidatorInterface:
    return ExpressionEmptyValidator()


@pytest.mark.parametrize(
    'expr',
    [
        (Number(1), Add(), Number(2)),
        (LParen(), Number(1), Pow(), Number(2), RParen()),
        (Number(1), Subtract(), LParen(), UnaryMinus(), Number(1), RParen()),
        (LParen(), RParen()),
    ],
)
def test_valid(validator: ValidatorInterface, expr):
    try:
        validator.validate(expr)
    except DomainError as e:
        pytest.fail(f'Корректное выражение не прошло валидацию: {e}')


@pytest.mark.parametrize(
    'expr',
    [
        (),
    ],
)
def test_invalid(validator: ValidatorInterface, expr):
    with pytest.raises(InvalidExpressionError):
        validator.validate(expr)
