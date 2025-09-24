from repository.rpn_converter import RPNConverter
from repository.token_parser import SpaceTokenizer
from usecase.rpn_calculator import RPNCalculatorUseCase


def test_rpn_calculator_usecase():
    parser = SpaceTokenizer()
    converter = RPNConverter()
    calc = RPNCalculatorUseCase(parser, converter)
    ans = calc.calculate('3 4 + 10 *')
    assert ans == 70
