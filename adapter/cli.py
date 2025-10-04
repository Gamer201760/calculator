from domain.error import DomainError
from usecase.calculator import CalculatorUsecase


class CliCalculator:
    """
    CLI Адаптер для калькулятора
    """

    def __init__(self, calculator: CalculatorUsecase, description: str):
        self._calculator = calculator
        self._description = description

    def run(self):
        """Запускает основной цикл приложения"""
        print(self._description)

        while True:
            try:
                line = input('>>> ')
                if line.lower() in ['exit', 'quit', 'q']:
                    break

                result = self._calculator.exec(line)
                print(f'Результат: {result}')

            except DomainError as e:
                print(f'Ошибка в выражении: {e}')
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f'Произошла непредвиденная системная ошибка: {e}')

        print('\nЗавершение работы')
