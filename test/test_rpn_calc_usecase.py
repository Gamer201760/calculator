from repository.operator import OperatorRepository
from repository.token_parser import SpaceTokenParser
from usecase.rpn_calculator import RPNCalculatorUseCase


def test_rpn_calculator_usecase():
    op = OperatorRepository()
    parser = SpaceTokenParser(op)
    calc = RPNCalculatorUseCase(parser)
    ans = calc.calculate('3 4 + 10 *')
    assert ans == 70
