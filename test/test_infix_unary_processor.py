import logging

import pytest

from domain.operator import Add, IntegerDivide, Multiply, Subtract
from domain.token import LParen, Number, RParen
from domain.unary import UnaryMinus, UnaryPlus
from repository.infix_unary_processor import InfixUnaryProcessor
from usecase.interface import ProcessorInterface

logger = logging.getLogger(__name__)


@pytest.fixture
def processor() -> ProcessorInterface:
    return InfixUnaryProcessor()


@pytest.mark.parametrize(
    'expr,expected',
    [
        (
            [Number(10), IntegerDivide(), Add(), Number(10)],
            [Number(10), IntegerDivide(), UnaryPlus(), Number(10)],
        ),
        (
            [Number(10), IntegerDivide(), Subtract(), Number(10)],
            [Number(10), IntegerDivide(), UnaryMinus(), Number(10)],
        ),
        (
            [Number(10), IntegerDivide(), Add()],
            [Number(10), IntegerDivide(), Add()],
        ),
        (
            [LParen(), Number(2), Add(), Number(3), RParen(), Multiply(), Number(4)],
            [LParen(), Number(2), Add(), Number(3), RParen(), Multiply(), Number(4)],
        ),
    ],
)
def test_unary(processor: ProcessorInterface, expr, expected):
    tokens = processor.process(expr)
    logger.debug(tokens)
    assert len(tokens) == len(expected)
    for t, e in zip(tokens, expected):
        assert isinstance(t, type(e))
        if isinstance(t, Number):
            assert t.value == e.value
