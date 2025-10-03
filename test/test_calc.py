import logging

import pytest

from domain.calculator import RPNCalculator
from repository.infix_unary_processor import InfixUnaryProcessor
from repository.re_parser import RegexTokenizer
from repository.shunting_yard import ShuntingYard
from repository.validator import (
    ExpressionBoundaryValidator,
    ExpressionEmptyValidator,
    OperatorSequenceValidator,
    ParenthesesValidator,
    RPNValidator,
    ValidatorFactory,
)
from usecase.infix_calculator import InfixCalculatorUsecase

logger = logging.getLogger(__name__)


@pytest.fixture
def calc() -> InfixCalculatorUsecase:
    return InfixCalculatorUsecase(
        tokenizer=RegexTokenizer(),
        calculator=RPNCalculator(),
        conveter=ShuntingYard(),
        processor=InfixUnaryProcessor(),
        pre_validator=ValidatorFactory(
            [
                ExpressionEmptyValidator(),
                ExpressionBoundaryValidator(),
                OperatorSequenceValidator(),
            ]
        ),
        post_validator=ParenthesesValidator(RPNValidator()),
    )


@pytest.mark.parametrize(
    'expr,expected',
    [
        ('-1 + (-2)', -3),
        ('1 + 2', 3),
        ('10 - 7', 3),
        ('4 * 5', 20),
        ('8 / 2', 4),
        ('7 / 2', 3.5),
        ('2 ^ 3', 8),
        ('-2 ^ 2', -4),
        ('(-2) ^ 2', 4),
        ('-(-1)', 1),
        ('9 // 2', 4),
        ('9 // 2.0', 4),
        ('9 % 2', 1),
        ('2 + 3 * 4', 14),
        ('( 2 + 3 ) * 4', 20),
        ('10 - 3 ^ 2', 1),
        ('18 // 4 + 2', 6),
        ('18 % 5 + 1', 4),
        ('0 / 5', 0),
        ('5 / 2', 2.5),
        ('5 // 2', 2),
        ('5 % 2', 1),
        ('2 ^ 0', 1),
        ('2 ^ 2', 4),
        ('0 ^ 5', 0),
        ('1 ^ 100', 1),
        ('1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10', 55),
        ('2 * 3 * 4 * 5', 120),
        ('100 - 10 * 9', 10),
        ('( 1 + 2 + 3 + 4 + 5 ) * 2', 30),
        ('2 ^ 3 ^ 2', 512),  # 2^(3^2) = 2^9 = 512
        ('1000 // 3 // 3', 111),
        ('1000%97', 30),
        ('50 * 2 + 100 / 4 - 30', 95),
        ('( 2 + 3 ) * ( 4 + 5 )', 45),
        ('( ( 2 + 3 ) * ( 4 + 5 ) ) ^ 2', 2025),
        (
            '1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10 + '
            '11 + 12 + 13 + 14 + 15 + 16 + 17 + 18 + 19 + 20',
            210,
        ),
        ('2 * 2 * 2 * 2 * 2 * 2 * 2 * 2 * 2 * 2', 1024),
        ('1000 - 1 - 1 - 1 - 1 - 1 - 1 - 1 - 1 - 1 - 1', 990),
        ('50 + 50 + 50 + 50 + 50 + 50 + 50 + 50 + 50 + 50', 500),
    ],
)
def test_calc(calc: InfixCalculatorUsecase, expr, expected):
    tokens = calc.exec(expr)
    logger.debug(tokens)
    assert tokens == expected
