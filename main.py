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

    pipeline: List[PipelineStepInterface]
    if args.rpn:
        pipeline = [
            ValidationStep(ExpressionEmptyValidator()),
            ValidationStep(ParenthesesValidator(RPNValidator())),
            ProcessingStep(RemoveParenProcessor()),
        ]
        description = """
Добро пожаловать в Калькулятор! (Режим Обратной Польской Нотации - RPN)

Введите выражение, где сначала идут операнды (числа), а затем оператор.

- Для унарного минуса используйте символ '~' (тильда).
- Для унарного плюса используйте символ '$'.

Для выхода введите 'exit' или 'quit'.

Пример 1: 5 2 3 + *  (инфиксная запись '5 * (2 + 3)')
Пример 2: 10 4 ~ -   (инфиксная запись '10 - (-4)')"""
    else:
        pipeline = [
            ValidationStep(ExpressionEmptyValidator()),
            ProcessingStep(InfixUnaryProcessor()),
            ValidationStep(ExpressionBoundaryValidator()),
            ValidationStep(OperatorSequenceValidator()),
            ConversionStep(ShuntingYard()),
            ValidationStep(RPNValidator()),
        ]
        description = """
Добро пожаловать в Калькулятор! (Режим Инфиксной Нотации)

Введите выражение в стандартной математической форме, используя операторы +, -, *, /, ^, //, % и скобки.
Для выхода введите 'exit' или 'quit'.

Пример: 5 * (-2 + 8) / 2"""

    calculator = CalculatorUsecase(
        tokenizer=RegexTokenizer(),
        pipeline=pipeline,
        calculator=RPNCalculator(),
    )
    cli = CliCalculator(calculator, description)
    cli.run()


if __name__ == '__main__':
    main()
