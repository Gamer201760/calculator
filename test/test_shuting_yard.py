from logging import getLogger

from domain.operator import Add, Multiply
from domain.token import Number
from repository.rpn_converter import ShuntingYard

logger = getLogger(__name__)


def test_shuting_yard():
    converter = ShuntingYard()
    rpn = converter.convert(
        [
            Number(3),
            Add(),
            Number(4),
            Multiply(),
            Number(10),
        ]
    )
    assert rpn == [
        Number(3),
        Number(4),
        Number(10),
        Multiply(),
        Add(),
    ]
