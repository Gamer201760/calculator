from domain.exception import DomainError
from repository.re_parser import RegexTokenizer
from repository.rpn_calculator import RPNCalculatorRepository
from repository.shunting_yard import ShuntingYard
from repository.validator import BalancedParenValidator
from usecase.rpn_calculator import RPNCalculatorUseCase


class CalculatorCLI:
    calculator: RPNCalculatorUseCase

    def run(self):
        """Запускает интерактивный режим"""
        while True:
            try:
                expression = input('> ').strip()

                if expression.lower() in {'quit', 'exit', 'q'}:
                    print('Goodbye!')
                    break

                if not expression:
                    continue

                result = self.calculator.calculate(expression)
                print(f'Result: {result}')

            except DomainError as e:
                print(f'Error: {e}')
            except KeyboardInterrupt:
                print('\nGoodbye!')
                break
            except Exception as e:
                print(f'Unexpected error: {e}')


class InfixCalculator(CalculatorCLI):
    def __init__(self) -> None:
        self.calculator = RPNCalculatorUseCase(
            parser=RegexTokenizer(),
            converter=ShuntingYard(),
            calc=RPNCalculatorRepository(),
            validators=[BalancedParenValidator()],
        )
        print('Вводите выражения в инфиксной записи (3 + 2) * 5 = 25')


class RPNCalculator(CalculatorCLI):
    def __init__(self) -> None:
        self.calculator = RPNCalculatorUseCase(
            parser=RegexTokenizer(),
            converter=ShuntingYard(),
            calc=RPNCalculatorRepository(),
            validators=[BalancedParenValidator()],
        )
        print('Вводите выражения в обратной польской нотации (3 2 +) 5 *')
