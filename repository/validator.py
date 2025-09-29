from typing import List

from domain.error import InsufficientOperandsError, InvalidExpressionError
from domain.token import LParen, Number, Operator, RParen, Token, UnaryOperator


class RPNValidator:
    """
    Валидирует список токенов в rpn (без скобок)
    """

    def validate(self, tokens: List[Token]) -> None:
        if not tokens:
            raise InvalidExpressionError('Невозможно валидировать пустое выражение')

        counter = 0
        for token in tokens:
            if isinstance(token, Number):
                counter += 1
            elif isinstance(token, UnaryOperator):
                if counter < 1:
                    raise InsufficientOperandsError(
                        f'Недостаточно операндов для унарного оператора "{token.symbol}"'
                    )
            elif isinstance(token, Operator):
                if counter < 2:
                    raise InsufficientOperandsError(
                        f'Недостаточно операндов для бинарного оператора "{token.symbol}"'
                    )
                counter -= 1
            elif isinstance(token, (LParen, RParen)):
                raise InvalidExpressionError(
                    'RPNValidator не должен обрабатывать скобки'
                )

        if counter != 1:
            raise InvalidExpressionError(
                'Выражение некорректно: в результате должно оставаться одно значение'
            )


class ParenthesesValidator:
    """
    Валидатор подвыражений в rpn (со скобками)
    """

    def __init__(self, rpn_validator: RPNValidator):
        self._rpn_validator = rpn_validator

    def validate(self, tokens: List[Token]) -> None:
        paren = 0
        sub_expr: List[List[Token]] = [[]]

        for token in tokens:
            if isinstance(token, LParen):
                paren += 1
                sub_expr.append([])
            elif isinstance(token, RParen):
                paren -= 1
                if paren < 0:
                    raise InvalidExpressionError(
                        'Несбалансированные скобки: лишняя закрывающая скобка'
                    )

                sub_expression = sub_expr.pop()
                self._rpn_validator.validate(sub_expression)
                sub_expr[-1].append(Number(value=0))

            else:
                sub_expr[-1].append(token)

        if paren != 0:
            raise InvalidExpressionError(
                'Несбалансированные скобки: не все скобки закрыты'
            )

        final_expr = sub_expr[0]
        if final_expr:
            self._rpn_validator.validate(final_expr)
