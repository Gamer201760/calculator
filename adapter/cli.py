from domain.exception import DomainError
from repository.rpn_converter import RPNConverter, ShuntingYard
from repository.token_parser import SpaceTokenizer
from usecase.rpn_calculator import RPNCalculatorUseCase


class SpaceCalculator:
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


class SpaceRPNCalculator(SpaceCalculator):
    """CLI адаптер для обратной польской записи"""

    def __init__(self):
        token_parser = SpaceTokenizer()
        converter = RPNConverter()
        self.calculator = RPNCalculatorUseCase(token_parser, converter)
        print('RPN Calculator')
        print("Enter RPN expressions (e.g., '3 4 + 2 *') or 'quit' to exit:")


class SpaceInfixCalculator(SpaceCalculator):
    """CLI адаптер для инфиксной записи"""

    def __init__(self):
        token_parser = SpaceTokenizer()
        converter = ShuntingYard()
        self.calculator = RPNCalculatorUseCase(token_parser, converter)
        print('Infix Calculator')
        print("Enter expressions (e.g., '(3 + 2) * 4') or 'quit' to exit:")
