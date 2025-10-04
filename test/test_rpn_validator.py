import pytest

from domain.error import (
    DomainError,
    InsufficientOperandsError,
    InvalidExpressionError,
)
from domain.operator import Add, Multiply, Pow, Subtract
from domain.token import Number
from domain.unary import UnaryMinus
from repository.validator import RPNValidator
from usecase.interface import ValidatorInterface


@pytest.fixture
def validator() -> ValidatorInterface:
    return RPNValidator()


@pytest.mark.parametrize(
    'expr',
    [
        (Number(5), Number(3), Add()),
        (Number(10), Number(5), Number(2), Multiply(), Subtract()),
        (Number(7), UnaryMinus()),
        (Number(5), Number(2), Pow(), UnaryMinus()),
        (Number(42),),
    ],
)
def test_valid(validator: ValidatorInterface, expr):
    """Корректно составленные RPN-выражения не вызывают ошибок."""
    try:
        validator.validate(expr)
    except DomainError as e:
        pytest.fail(f'Корректное выражение не прошло валидацию: {e}')


@pytest.mark.parametrize(
    'expr',
    [
        (Add(), Number(2), Number(3)),
        (Number(5), Subtract()),
        (UnaryMinus(), Number(5)),
        (Number(5), Number(3), Add(), Multiply()),
        (UnaryMinus(),),
    ],
)
def test_invalid_insufficient_operands(validator: ValidatorInterface, expr):
    with pytest.raises(InsufficientOperandsError):
        validator.validate(expr)


@pytest.mark.parametrize(
    'expr',
    [
        (Number(5), Number(3)),
        (Number(1), Number(2), Number(3), Add()),
    ],
)
def test_invalid_final_stack_count(validator: ValidatorInterface, expr):
    """Выражения, оставляющие в стеке не 1 значение, должны выкидывать ошибку"""
    with pytest.raises(InvalidExpressionError):
        validator.validate(expr)
