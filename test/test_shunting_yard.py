from logging import getLogger

from domain.operator import Add, Multiply
from domain.token import LParen, Number, RParen
from repository.rpn_converter import ShuntingYard

logger = getLogger(__name__)


def test_shunting_yard():
    converter = ShuntingYard()
    rpn = converter.convert(
        [
            LParen(),
            Number(3),
            Add(),
            Number(4),
            RParen(),
            Multiply(),
            Number(10),
        ]
    )
    logger.debug(rpn)
    assert rpn == [
        Number(3),
        Number(4),
        Add(),
        Number(10),
        Multiply(),
    ]
