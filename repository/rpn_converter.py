from typing import Dict, List

from domain.operator import Add, Divide, Multiply, Subtract
from domain.token import LParen, Number, Operator, RParen, Token


class ShuntingYard:
    """Алгоритм сортировочной станции для преобразования инфиксной записи в обратную польскую последовательность"""

    def __init__(self) -> None:
        # Приоритет операторов (чем больше число, тем выше приоритет)
        self.precedence: Dict[Operator, int] = {
            Add(): 1,
            Subtract(): 1,
            Multiply(): 2,
            Divide(): 2,
        }

        # Ассоциативность операторов (True - левая, False - правая)
        self.left_associative: Dict[Operator, bool] = {
            Add(): True,
            Subtract(): True,
            Multiply(): True,
            Divide(): True,
        }

    def convert(self, tokens: List) -> List[Token]:
        """
        Преобразует список токенов из инфиксной записи в постфиксную (RPN)

        Входные токены могут быть:
        - Number: числа
        - Operator: операторы (+, -, *, /, ^)
        - LeftParen/RightParen: скобки

        Возвращает Number и Operator токены в RPN порядке (скобки исключаются)
        """
        output_queue: List[Token] = []
        operator_stack: List = []

        for token in tokens:
            if isinstance(token, Number):
                # Числа идут прямо в выходную очередь
                output_queue.append(token)

            elif isinstance(token, Operator):
                # Обрабатываем операторы согласно приоритету и ассоциативности
                while (
                    operator_stack
                    and isinstance(operator_stack[-1], Operator)
                    and self._should_pop_operator(token, operator_stack[-1])
                ):
                    output_queue.append(operator_stack.pop())

                operator_stack.append(token)

            elif isinstance(token, LParen):
                # Левые скобки всегда помещаются в стек
                operator_stack.append(token)

            elif isinstance(token, RParen):
                # Правые скобки: выталкиваем операторы до левой скобки
                while operator_stack and not isinstance(operator_stack[-1], LParen):
                    output_queue.append(operator_stack.pop())

                # Удаляем левую скобку из стека (она не попадает в выход)
                if operator_stack and isinstance(operator_stack[-1], LParen):
                    operator_stack.pop()
                else:
                    raise ValueError(
                        'Несбалансированные скобки: не найдена левая скобка'
                    )

        # Выталкиваем все оставшиеся операторы из стека
        while operator_stack:
            if isinstance(operator_stack[-1], LParen):
                raise ValueError('Несбалансированные скобки: лишняя левая скобка')
            output_queue.append(operator_stack.pop())

        return output_queue

    def _should_pop_operator(self, current_op: Operator, stack_op: Operator) -> bool:
        """
        Определяет, нужно ли вытолкнуть оператор из стека
        """
        current_prec = self.precedence.get(current_op, 0)
        stack_prec = self.precedence.get(stack_op, 0)

        # Если приоритет оператора в стеке больше
        if stack_prec > current_prec:
            return True

        # Если приоритеты равны и текущий оператор левоассоциативен
        if stack_prec == current_prec and self.left_associative.get(current_op, True):
            return True

        return False


class RPNConverter:
    """Конвертер - заглушка для уже обратной польской записи"""

    def convert(self, tokens: List[Token]) -> List[Token]:
        return tokens
