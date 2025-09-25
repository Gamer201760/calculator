import pytest

from domain.operator import (
    Add,
    Divide,
    IntegerDivide,
    Modulo,
    Multiply,
    Pow,
    Subtract,
)
from domain.token import LParen, Number, RParen
from repository.re_parser import RegexTokenizer


@pytest.mark.parametrize(
    'expr,expected',
    [
        ('1 + 2', [Number(1), Add(), Number(2)]),
        ('3 - 4', [Number(3), Subtract(), Number(4)]),
        ('5 * 6', [Number(5), Multiply(), Number(6)]),
        ('7 / 8', [Number(7), Divide(), Number(8)]),
        ('2 ^ 3', [Number(2), Pow(), Number(3)]),
        ('9 // 2', [Number(9), IntegerDivide(), Number(2)]),
        ('10 % 3', [Number(10), Modulo(), Number(3)]),
        (
            '(1 + 2) * 3',
            [LParen(), Number(1), Add(), Number(2), RParen(), Multiply(), Number(3)],
        ),
        (
            '4 + (5 * 6)',
            [Number(4), Add(), LParen(), Number(5), Multiply(), Number(6), RParen()],
        ),
        (
            '(7 - 8) / (9 + 1)',
            [
                LParen(),
                Number(7),
                Subtract(),
                Number(8),
                RParen(),
                Divide(),
                LParen(),
                Number(9),
                Add(),
                Number(1),
                RParen(),
            ],
        ),
        (
            '1 + 2 - 3 * 4 / 5 ^ 6',
            [
                Number(1),
                Add(),
                Number(2),
                Subtract(),
                Number(3),
                Multiply(),
                Number(4),
                Divide(),
                Number(5),
                Pow(),
                Number(6),
            ],
        ),
        (
            '(1 + 2) * (3 - 4) / (5 % 2) ^ 2',
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
                Divide(),
                LParen(),
                Number(5),
                Modulo(),
                Number(2),
                RParen(),
                Pow(),
                Number(2),
            ],
        ),
        (
            '10 // 3 + 4 * (5 - 6) / 7 ^ 2 - 8 % 3',
            [
                Number(10),
                IntegerDivide(),
                Number(3),
                Add(),
                Number(4),
                Multiply(),
                LParen(),
                Number(5),
                Subtract(),
                Number(6),
                RParen(),
                Divide(),
                Number(7),
                Pow(),
                Number(2),
                Subtract(),
                Number(8),
                Modulo(),
                Number(3),
            ],
        ),
        (
            '((1 + 2) * 3 - 4) / (5 + (6 - 7) * 8)',
            [
                LParen(),
                LParen(),
                Number(1),
                Add(),
                Number(2),
                RParen(),
                Multiply(),
                Number(3),
                Subtract(),
                Number(4),
                RParen(),
                Divide(),
                LParen(),
                Number(5),
                Add(),
                LParen(),
                Number(6),
                Subtract(),
                Number(7),
                RParen(),
                Multiply(),
                Number(8),
                RParen(),
            ],
        ),
    ],
)
def test_tokenize(expr, expected):
    tokens = RegexTokenizer().parse(expr)

    # Проверяем типы и значения токенов
    assert len(tokens) == len(expected)
    for t, e in zip(tokens, expected):
        assert isinstance(t, type(e))
        if isinstance(t, Number):
            assert t.value == e.value
