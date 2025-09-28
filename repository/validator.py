from typing import List

from domain.exception import InsufficientOperandsError, InvalidExpressionError
from domain.token import LParen, Number, Operator, RParen, Token, UnaryOperator


class BalancedParenValidator:
    def validate(self, tokens: List[Token]) -> None:
        paren_count = 0
        for token in tokens:
            if isinstance(token, LParen):
                paren_count += 1
            elif isinstance(token, RParen):
                paren_count -= 1
                if paren_count < 0:
                    raise InvalidExpressionError('Unmatched closing parenthesis')

        if paren_count > 0:
            raise InvalidExpressionError('Unmatched opening parenthesis')


class OperatorPlacementValidator:
    """Проверяет последовательность операторов"""

    def validate(self, tokens: List[Token]) -> None:
        prev_token = None
        for i, token in enumerate(tokens):
            if isinstance(token, Operator):
                if i == 0 or i == len(tokens) - 1:
                    raise InvalidExpressionError(
                        f"Operator '{token.symbol}' at invalid position"
                    )

                if isinstance(prev_token, Operator):
                    raise InvalidExpressionError('Consecutive operators not allowed')

            prev_token = token


class ParenthesesValidator:
    """
    Валидатор для выражений в обратной польской нотации (RPN),
    который проверяет сбалансированность скобок и корректность
    подвыражений внутри них.
    """

    def validate(self, tokens: List[Token]) -> None:
        """
        Валидирует список токенов
        """
        paren_balance = 0
        sub_expression_stack: List[List[Token]] = []

        for token in tokens:
            if isinstance(token, LParen):
                paren_balance += 1
                sub_expression_stack.append([])
            elif isinstance(token, RParen):
                paren_balance -= 1
                if paren_balance < 0:
                    raise InvalidExpressionError(
                        'Несбалансированные скобки: лишняя закрывающая скобка'
                    )

                if not sub_expression_stack:
                    raise InvalidExpressionError(
                        'Несбалансированные скобки: лишняя закрывающая скобка'
                    )

                sub_expression = sub_expression_stack.pop()
                self._validate_sub_expression(sub_expression)

                if sub_expression_stack:
                    sub_expression_stack[-1].append(Number(0))

            elif sub_expression_stack:
                sub_expression_stack[-1].append(token)

        if paren_balance != 0:
            raise InvalidExpressionError(
                'Несбалансированные скобки: не все скобки закрыты'
            )

    def _validate_sub_expression(self, tokens: List[Token]) -> None:
        """Валидирует отдельное подвыражение"""
        if not tokens:
            raise InvalidExpressionError('Пустое подвыражение в скобках')

        operand_stack = []
        for token in tokens:
            if isinstance(token, Number):
                operand_stack.append(token)
            elif isinstance(token, UnaryOperator):
                if not operand_stack:
                    raise InsufficientOperandsError(
                        f'Недостаточно операндов для унарного оператора "{token.symbol}"'
                    )
                operand_stack.pop()
                operand_stack.append(Number(0))
            elif isinstance(token, Operator):
                if len(operand_stack) < 2:
                    raise InsufficientOperandsError(
                        f'Недостаточно операндов для бинарного оператора "{token.symbol}"'
                    )
                operand_stack.pop()
                operand_stack.pop()
                operand_stack.append(Number(0))

        if len(operand_stack) != 1:
            raise InvalidExpressionError(
                'Некорректное выражение в скобках: в конце должно оставаться одно значение'
            )
