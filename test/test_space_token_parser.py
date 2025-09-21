from logging import getLogger

from domain.operator import Add, Multiply
from domain.token import Number
from repository.operator import OperatorRepository
from repository.token_parser import SpaceTokenParser

logger = getLogger(__name__)


def test_infix():
    op = OperatorRepository()
    parser = SpaceTokenParser(op)
    infix = parser.parse('3 + 4 * 10')
    logger.debug(infix)
    assert infix == [Number(3), Add(), Number(4), Multiply(), Number(10)]


def test_rpn():
    op = OperatorRepository()
    parser = SpaceTokenParser(op)
    rpn = parser.parse('3 4 + 10 *')
    logger.debug(rpn)
    assert rpn == [Number(3), Number(4), Add(), Number(10), Multiply()]
