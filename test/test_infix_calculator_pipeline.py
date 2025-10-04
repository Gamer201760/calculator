import logging
from typing import List

import pytest

from domain.calculator import RPNCalculator
from domain.error import CalculationError, InvalidExpressionError, InvalidTokenError
from repository.infix_unary_processor import InfixUnaryProcessor
from repository.re_parser import RegexTokenizer
from repository.shunting_yard import ShuntingYard
from repository.validator import (
    ExpressionBoundaryValidator,
    ExpressionEmptyValidator,
    OperatorSequenceValidator,
    RPNValidator,
)
from usecase.calculator import CalculatorUsecase
from usecase.pipeline import (
    ConversionStep,
    PipelineStepInterface,
    ProcessingStep,
    ValidationStep,
)

logger = logging.getLogger(__name__)


@pytest.fixture
def calc() -> CalculatorUsecase:
    pipeline: List[PipelineStepInterface] = [
        ValidationStep(ExpressionEmptyValidator()),
        ProcessingStep(InfixUnaryProcessor()),
        ValidationStep(ExpressionBoundaryValidator()),
        ValidationStep(OperatorSequenceValidator()),
        ConversionStep(ShuntingYard()),
        ValidationStep(RPNValidator()),
    ]
    return CalculatorUsecase(
        tokenizer=RegexTokenizer(),
        pipeline=pipeline,
        calculator=RPNCalculator(),
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
        ('1 + 2', 3),
        ('2 + 3 * 4', 14),
        ('5 / 2', 2.5),
        ('( 2 + 3 ) * 4', 20),
        ('-2', -2.0),
        ('-(-2)', 2.0),
        ('-2 ^ 2', -4),
        ('(-2) ^ 2', 4),
        ('10 * (-5)', -50),
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
def test_calc(calc: CalculatorUsecase, expr, expected):
    tokens = calc.exec(expr)
    logger.debug(tokens)
    assert calc.exec(expr) == pytest.approx(expected)


@pytest.mark.parametrize(
    'expr,expected_exception',
    [
        # неизвестные символы
        ('5 @ 2', InvalidTokenError),
        ('1..2 + 3', InvalidTokenError),
        ('abc + 5', InvalidTokenError),
        # некорректное выражение
        ('', InvalidExpressionError),
        ('   ', InvalidExpressionError),
        # некорректные границы выражения
        ('* 5 + 2', InvalidExpressionError),
        ('5 + 2 *', InvalidExpressionError),
        ('5 +', InvalidExpressionError),
        # некорректная последовательность операторов
        ('5 * / 2', InvalidExpressionError),
        (
            '5 + - 2',
            InvalidExpressionError,
        ),
        ('5 // +', InvalidExpressionError),  # унарный оператор без числа после
        # несбалансированные скобки ---
        ('(5 + 2', InvalidExpressionError),
        ('5 + 2)', InvalidExpressionError),
        ('5 * (', InvalidExpressionError),
        (') 5 + 2 (', InvalidExpressionError),
        # пустые скобки или лишние операнды ---
        ('()', InvalidExpressionError),
        ('5 6', InvalidExpressionError),
        ('(5 6)', InvalidExpressionError),
        # ошибки вычисления
        ('5 / 0', CalculationError),
        ('10 / (3 - 3)', CalculationError),
        ('1 // 0', CalculationError),
        ('1 % 0', CalculationError),
        ('1000000 ^ 1000000', CalculationError),
    ],
)
def test_errors(calc: CalculatorUsecase, expr: str, expected_exception: type):
    with pytest.raises(expected_exception):
        calc.exec(expr)
