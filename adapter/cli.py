from domain.exception import DomainError
from repository.operator import OperatorRepository
from repository.rpn_converter import ShuntingYard
from repository.token_parser import SpaceTokenizer
from usecase.rpn_calculator import RPNCalculatorUseCase


class CLIAdapter:
    """CLI адаптер для RPN калькулятора"""

    def __init__(self):
        operator_repo = OperatorRepository()
        token_parser = SpaceTokenizer(operator_repo)
        converter = ShuntingYard()
        self.calculator = RPNCalculatorUseCase(token_parser, converter)

    def run(self):
        """Запускает интерактивный режим"""
        print('RPN Calculator')
        print("Enter RPN expressions (e.g., '3 4 + 2 *') or 'quit' to exit:")

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
