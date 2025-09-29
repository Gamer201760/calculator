import pytest

from domain.error import (
    DomainError,
    InsufficientOperandsError,
    InvalidExpressionError,
)
from domain.operator import Add, Multiply, Subtract
from domain.token import LParen, Number, RParen
from domain.unary import UnaryMinus
from repository.validator import ParenthesesValidator, RPNValidator


@pytest.fixture
def validator() -> ParenthesesValidator:
    return ParenthesesValidator(RPNValidator())


@pytest.mark.parametrize(
    'tokens',
    [
        ([LParen(), Number(5), Number(3), Add(), RParen()]),
        (
            [
                LParen(),
                Number(5),
                LParen(),
                Number(3),
                Number(2),
                Multiply(),
                RParen(),
                Add(),
                RParen(),
            ]
        ),
        ([LParen(), Number(10), UnaryMinus(), RParen()]),
        ([Number(5), Number(3), Add()]),
        (
            [
                LParen(),
                Number(1),
                Number(1),
                Add(),
                RParen(),
                LParen(),
                Number(2),
                Number(2),
                Multiply(),
                RParen(),
                Subtract(),
            ]
        ),
    ],
)
def test_valid_expressions(validator, tokens):
    """Корректно составленные выражения не вызывают ошибок"""
    try:
        validator.validate(tokens)
    except DomainError as e:
        pytest.fail(f'Корректное выражение не прошло валидацию: {e}')


def test_empty_parentheses_throws_error(validator):
    """Пустое выражение () вызывает InvalidExpressionError"""
    tokens = [LParen(), RParen()]
    with pytest.raises(InvalidExpressionError):
        validator.validate(tokens)


def test_unbalanced_extra_closing_paren_throws_error(validator):
    """Выражение с лишней закрывающей скобкой вызывает InvalidExpressionError"""
    tokens = [Number(5), Number(3), Add(), RParen()]
    with pytest.raises(InvalidExpressionError):
        validator.validate(tokens)


def test_unbalanced_extra_opening_paren_throws_error(validator):
    """Выражение с лишней открывающей скобкой вызывает InvalidExpressionError"""
    tokens = [LParen(), Number(5), Number(3), Add()]
    with pytest.raises(InvalidExpressionError):
        validator.validate(tokens)


@pytest.mark.parametrize(
    'tokens',
    [
        ([Number(5), Number(3), Add(), Add(), Add()]),
        ([LParen(), Number(5), Add(), RParen()]),
        ([LParen(), Add(), RParen()]),
        ([LParen(), Number(1), LParen(), Subtract(), RParen(), RParen()]),
    ],
)
def test_insufficient_operands_for_binary_op(validator, tokens):
    """Не хватает операндов для бинарных операторов"""
    with pytest.raises(InsufficientOperandsError):
        validator.validate(tokens)


@pytest.mark.parametrize(
    'tokens',
    [
        (LParen(), UnaryMinus(), RParen()),
        (UnaryMinus(),),
    ],
)
def test_insufficient_operands_for_unary_op(validator, tokens):
    """Не хватает операндов для унарных операторов"""
    with pytest.raises(InsufficientOperandsError):
        validator.validate(tokens)


def test_sub_expression_not_resolving_to_one_value(validator):
    """(5 3) вызывает ошибку, т.к в стеке остается два числа"""
    tokens = [LParen(), Number(5), Number(3), RParen()]
    with pytest.raises(InvalidExpressionError):
        validator.validate(tokens)
