import pytest

from domain.error import InvalidExpressionError
from domain.operator import Add, Divide, IntegerDivide, Modulo, Multiply, Pow, Subtract
from domain.token import LParen, Number, RParen
from repository.validator import BalancedParenValidator, OperatorPlacementValidator


@pytest.mark.parametrize(
    'tokens',
    [
        [Number(1), Add(), Number(2)],
        [LParen(), Number(1), Add(), Number(2), RParen()],
        [
            LParen(),
            LParen(),
            Number(1),
            Add(),
            Number(2),
            RParen(),
            Multiply(),
            Number(3),
            RParen(),
        ],
        # Несколько скобочных групп
        [
            LParen(),
            Number(1),
            Add(),
            Number(2),
            RParen(),
            Multiply(),
            LParen(),
            Number(3),
            Subtract(),
            Number(4),
            RParen(),
        ],
        # Сложное выражение
        [
            LParen(),
            LParen(),
            Number(1),
            Add(),
            Number(2),
            RParen(),
            Multiply(),
            LParen(),
            Number(3),
            Subtract(),
            Number(4),
            RParen(),
            RParen(),
        ],
        [
            LParen(),
            LParen(),
            LParen(),
            LParen(),
            LParen(),
            RParen(),
            RParen(),
            RParen(),
            RParen(),
            RParen(),
        ],
    ],
)
def test_validate_balanced(tokens):
    """Корректные выражения не должны вызывать ошибок"""
    validator = BalancedParenValidator()
    validator.validate(tokens)


@pytest.mark.parametrize(
    'tokens',
    [
        [Number(1), Add(), RParen(), Number(2)],
        [LParen(), Number(1), Add(), Number(2)],
        [Number(1), Add(), Number(2), RParen()],
        [LParen(), Number(1), Add(), RParen(), Number(2), RParen()],
        [LParen(), LParen(), Number(1), Add(), Number(2), RParen(), Number(3)],
        [LParen()],
        [RParen()],
        [LParen(), RParen(), RParen()],
        [RParen(), LParen()],
    ],
)
def test_validate_unbalanced(tokens):
    """Некорректные выражения должны кидать InvalidExpressionError"""
    validator = BalancedParenValidator()
    with pytest.raises(InvalidExpressionError):
        validator.validate(tokens)


@pytest.mark.parametrize(
    'tokens',
    [
        [Add(), Number(1), Number(2)],
        [Subtract(), Number(3)],
        [Multiply(), Number(4), Number(5)],
        [Number(1), Add()],
        [Number(2), Subtract()],
        [Number(3), Divide()],
        [Number(1), Add(), Multiply(), Number(2)],
        [Number(3), Subtract(), Divide(), Number(4)],
        [Number(5), Pow(), Pow(), Number(6)],
        [Add(), Add(), Number(1)],
        [Number(1), Multiply(), Divide()],
    ],
)
def test_operator_placement_invalid(tokens):
    """Некорректные выражения должны кидать InvalidExpressionError"""
    validator = OperatorPlacementValidator()
    with pytest.raises(InvalidExpressionError):
        validator.validate(tokens)


@pytest.mark.parametrize(
    'tokens',
    [
        [Number(1), Add(), Number(2)],
        [Number(3), Subtract(), Number(4)],
        [Number(5), Multiply(), Number(6)],
        [Number(7), Divide(), Number(8)],
        [Number(1), Add(), Number(2), Multiply(), Number(3), Subtract(), Number(4)],
        [Number(10), Divide(), Number(2), Add(), Number(3), Pow(), Number(2)],
        [Number(9), IntegerDivide(), Number(2), Add(), Number(3), Modulo(), Number(2)],
    ],
)
def test_operator_placement_valid(tokens):
    """Корректные выражения не должны кидать исключения"""
    validator = OperatorPlacementValidator()
    validator.validate(tokens)
