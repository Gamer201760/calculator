import argparse

from adapter.cli import CliAdapter
from domain.calculator import RPNCalculator
from repository.re_parser import RegexTokenizer
from repository.validator import ParenthesesValidator, RPNValidator
from usecase.rpn_calculator import RPNCalculatorUsecase


def main():
    """Точка входа в программу"""
    parser = argparse.ArgumentParser(
        prog='Calculator',
    )
    parser.add_argument('--rpn', action='store_true')
    # args = parser.parse_args()
    cli = CliAdapter(
        calculator=RPNCalculatorUsecase(
            tokenizer=RegexTokenizer(),
            calculator=RPNCalculator(),
            validators=[ParenthesesValidator(RPNValidator())],
        ),
    )
    cli.run()


if __name__ == '__main__':
    main()
