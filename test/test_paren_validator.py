import pytest

from domain.exception import InvalidExpressionError
from domain.operator import Add, Multiply, Subtract
from domain.token import LParen, Number, RParen
from repository.validator import BalancedParenValidator


@pytest.mark.parametrize(
    'tokens',
    [
        # Нет скобок
        [Number(1), Add(), Number(2)],
        # Простая пара скобок
        [LParen(), Number(1), Add(), Number(2), RParen()],
        # Вложенные скобки
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
