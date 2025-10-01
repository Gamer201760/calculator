from logging import getLogger

import pytest

from domain.operator import Add, Pow
from domain.token import Number
from domain.unary import UnaryMinus
from repository.shunting_yard import ShuntingYard

logger = getLogger(__name__)


@pytest.fixture
def converter() -> ShuntingYard:
    return ShuntingYard()


@pytest.mark.parametrize(
    'expr,expected',
    [
        ((Number(2), Add(), Number(3)), (Number(2), Number(3), Add())),
        (
            (Number(2), Add(), UnaryMinus(), Number(3)),
            (Number(2), Number(3), UnaryMinus(), Add()),
        ),
        (
            (UnaryMinus(), Number(2), Pow(), Number(2)),
            (Number(2), Number(2), Pow(), UnaryMinus()),
        ),
    ],
)
def test_shunting_yard(converter: ShuntingYard, expr, expected):
    rpn = converter.convert(expr)
    logger.debug(rpn)
    assert len(rpn) == len(expected)
    for t, e in zip(rpn, expected):
        assert isinstance(t, type(e))
        if isinstance(t, Number):
            assert t.value == e.value
