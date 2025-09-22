from typing import Dict, List

from domain.token import Number, Operator, Token


class ShuntingYard:
    """Алгоритм сортировочной станции для преобразования инфиксной записи в обратную польскую последовательность"""

    def __init__(self):
        # Приоритет операторов (чем больше число, тем выше приоритет)
        self.precedence: Dict[str, int] = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

        # Ассоциативность операторов (True - левая, False - правая)
        self.left_associative: Dict[str, bool] = {
            '+': True,
            '-': True,
            '*': True,
            '/': True,
            '^': False,  # возведение в степень правоассоциативно
        }

    def convert(self, tokens: List) -> List[Token]:
        """
        Преобразует список токенов из инфиксной записи в постфиксную (RPN)

        Входные токены могут быть:
        - Number: числа
        - Operator: операторы (+, -, *, /, ^)

        Возвращает Number и Operator токены в RPN порядке
        """
        output_queue: List[Token] = []
        operator_stack: List[Operator] = []

        for token in tokens:
            if isinstance(token, Number):
                # Числа идут прямо в выходную очередь
                output_queue.append(token)

            elif isinstance(token, Operator):
                # Обрабатываем операторы согласно приоритету и ассоциативности
                while operator_stack and self._should_pop_operator(
                    token, operator_stack[-1]
                ):
                    output_queue.append(operator_stack.pop())

                operator_stack.append(token)

        # Выталкиваем все оставшиеся операторы из стека
        while operator_stack:
            output_queue.append(operator_stack.pop())

        return output_queue

    def _should_pop_operator(self, current_op: Operator, stack_op: Operator) -> bool:
        """
        Определяет, нужно ли вытолкнуть оператор из стека
        """
        current_symbol = current_op.symbol()
        stack_symbol = stack_op.symbol()

        current_prec = self.precedence.get(current_symbol, 0)
        stack_prec = self.precedence.get(stack_symbol, 0)

        # Если приоритет оператора в стеке больше
        if stack_prec > current_prec:
            return True

        # Если приоритеты равны и текущий оператор левоассоциативен
        if stack_prec == current_prec and self.left_associative.get(
            current_symbol, True
        ):
            return True

        return False


class RPNConverter:
    """Конвертер - заглушка для уже обратной польской записи"""

    def convert(self, tokens: List[Token]) -> List[Token]:
        return tokens
