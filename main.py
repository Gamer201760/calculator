import argparse
from typing import List

from adapter.cli import CliCalculator
from domain.calculator import RPNCalculator
from repository.infix_unary_processor import InfixUnaryProcessor
from repository.re_parser import RegexTokenizer
from repository.remove_paren_processor import RemoveParenProcessor
from repository.shunting_yard import ShuntingYard
from repository.validator import (
    ExpressionBoundaryValidator,
    ExpressionEmptyValidator,
    OperatorSequenceValidator,
    ParenthesesValidator,
    RPNValidator,
)
from usecase.calculator import CalculatorUsecase
from usecase.pipeline import (
    ConversionStep,
    PipelineStepInterface,
    ProcessingStep,
    ValidationStep,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog='Calculator',
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
Консольный калькулятор для вычисления математических выражений
Поддерживает два режима: стандартную инфиксную нотацию (по умолчанию)
и обратную польскую нотацию (RPN)
        """,
    )
    parser.add_argument(
        '--rpn',
        action='store_true',
        help='Запустить калькулятор в Обратной Польской Нотации (RPN)',
    )
    args = parser.parse_args()

    infix_pipeline: List[PipelineStepInterface] = [
        ValidationStep(ExpressionEmptyValidator()),
        ProcessingStep(InfixUnaryProcessor()),
        ValidationStep(ExpressionBoundaryValidator()),
        ValidationStep(OperatorSequenceValidator()),
        ConversionStep(ShuntingYard()),
        ValidationStep(RPNValidator()),
    ]
    rpn_pipeline: List[PipelineStepInterface] = [
        ValidationStep(ExpressionEmptyValidator()),
        ValidationStep(ParenthesesValidator(RPNValidator())),
        ProcessingStep(RemoveParenProcessor()),
    ]
    calculator = CalculatorUsecase(
        tokenizer=RegexTokenizer(),
        pipeline=rpn_pipeline if args.rpn else infix_pipeline,
        calculator=RPNCalculator(),
    )
    cli = CliCalculator(calculator)
    cli.run()


if __name__ == '__main__':
    main()
