from domain.error import DomainError
from usecase.rpn_calculator import RPNCalculatorUsecase


class CliAdapter:
    """
    CLI Адаптер для RPN калькулятора
    """

    def __init__(self, calculator: RPNCalculatorUsecase):
        self._calculator = calculator

    def run(self):
        """Запускает основной цикл приложения."""
        print('Добро пожаловать в RPN Калькулятор')
        print("Введите выражение или 'exit' для выхода")
        print('Пример: 10 ( 5 3 - ) * 2 /')

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
