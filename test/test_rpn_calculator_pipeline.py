import logging
from typing import List

import pytest

from domain.calculator import RPNCalculator
from domain.error import (
    CalculationError,
    InsufficientOperandsError,
    InvalidExpressionError,
    InvalidTokenError,
)
from repository.re_parser import RegexTokenizer
from repository.remove_paren_processor import RemoveParenProcessor
from repository.validator import (
    ExpressionEmptyValidator,
    ParenthesesValidator,
    RPNValidator,
)
from usecase.calculator import CalculatorUsecase
from usecase.pipeline import (
    PipelineStepInterface,
    ProcessingStep,
    ValidationStep,
)

logger = logging.getLogger(__name__)


@pytest.fixture
def calc() -> CalculatorUsecase:
    pipeline: List[PipelineStepInterface] = [
        ValidationStep(ExpressionEmptyValidator()),
        ValidationStep(ParenthesesValidator(RPNValidator())),
        ProcessingStep(RemoveParenProcessor()),
    ]
    return CalculatorUsecase(
        tokenizer=RegexTokenizer(),
        pipeline=pipeline,
        calculator=RPNCalculator(),
    )


@pytest.mark.parametrize(
    'expr,expected',
    [
        ('5 3 +', 8),
        ('10 5 2 * -', 0),
        ('7 2 /', 3.5),
        ('1.5 2.5 +', 4.0),
        ('42 ~', -42),
        ('42 $', 42),
        ('10 ~ ~', 10),
        ('10 4 ~ -', 14),
        ('5 2 ^ ~', -25),
        ('42', 42),
        ('0 5 /', 0),
    ],
)
def test_calc(calc: CalculatorUsecase, expr, expected):
    tokens = calc.exec(expr)
    logger.debug(tokens)
    assert calc.exec(expr) == pytest.approx(expected)


@pytest.mark.parametrize(
    'expr,expected_exception',
    [
        ('5 @ 2', InvalidTokenError),
        ('a b +', InvalidTokenError),
        ('', InvalidExpressionError),
        ('   ', InvalidExpressionError),
        ('* 5 3', InsufficientOperandsError),
        ('5 *', InsufficientOperandsError),
        ('~', InsufficientOperandsError),
        (
            '5 3 + *',
            InsufficientOperandsError,
        ),
        ('5 ~ *', InsufficientOperandsError),
        ('5 3', InvalidExpressionError),
        ('1 2 3 +', InvalidExpressionError),
        (
            '5 ~ 3',
            InvalidExpressionError,
        ),
        (
            '5 + 3',
            InsufficientOperandsError,
        ),
        ('(5 + 3)', InsufficientOperandsError),
        ('5 0 /', CalculationError),
        ('10 3 3 - /', CalculationError),
        ('1 0 //', CalculationError),
        ('1 0 %', CalculationError),
    ],
)
def test_errors(calc: CalculatorUsecase, expr: str, expected_exception: type):
    with pytest.raises(expected_exception):
        calc.exec(expr)
