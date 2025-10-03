from itertools import pairwise
from typing import List

from domain.error import InsufficientOperandsError, InvalidExpressionError
from domain.token import LParen, Number, Operator, RParen, Token, UnaryOperator


class RPNValidator:
    """
    Валидирует список токенов в rpn (без скобок)
    """

    def validate(self, tokens: List[Token]) -> None:
        c = 0
        for token in tokens:
            if isinstance(token, Number):
                c += 1
            elif isinstance(token, UnaryOperator):
                if c < 1:
                    raise InsufficientOperandsError(
                        f'Недостаточно операндов для унарного оператора "{token.symbol}"'
                    )
            elif isinstance(token, Operator):
                if c < 2:
                    raise InsufficientOperandsError(
                        f'Недостаточно операндов для бинарного оператора "{token.symbol}"'
                    )
                c -= 1
            elif isinstance(token, (LParen, RParen)):
                raise InvalidExpressionError(
                    'RPNValidator не должен обрабатывать скобки'
                )

        if c != 1:
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


class OperatorSequenceValidator:
    """
    Валидатор последовательности операторов

    Проверяет, что операторы не стоят рядом некорректно:
    - Два бинарных оператора не могут стоять рядом
    - Два унарных оператора не могут стоять рядом
    - Бинарный и унарный операторы не могут стоять рядом
    - Унарный и бинарный операторы не могут стоять рядом
    """

    def validate(self, tokens: List[Token]) -> None:
        for curr, next_token in pairwise(tokens):
            if self._is_invalid_operator_sequence(curr, next_token):
                raise InvalidExpressionError(
                    f'Некорректная последовательность операторов: {curr} {next_token}'
                )

    def _is_invalid_operator_sequence(self, curr: Token, next_token: Token) -> bool:
        """Является ли последовательность двух токенов некорректной"""
        # Два бинарных
        if isinstance(curr, Operator) and isinstance(next_token, Operator):
            return True

        # Два унарных
        if isinstance(curr, UnaryOperator) and isinstance(next_token, UnaryOperator):
            return True

        # Бинарный оператор, унарный
        if isinstance(curr, Operator) and isinstance(next_token, UnaryOperator):
            return True

        # Унарный оператор, бинарный
        if isinstance(curr, UnaryOperator) and isinstance(next_token, Operator):
            return True

        return False


class ExpressionBoundaryValidator:
    """
    Валидатор границ выражения
    Проверяет, что первый и последний токены могут начинать/заканчивать выражение
    """

    def validate(self, tokens: List[Token]) -> None:
        self._validate_first_token(tokens[0])
        self._validate_last_token(tokens[-1])

    def _validate_first_token(self, token: Token) -> None:
        """Первый токен может начинать выражение"""
        if isinstance(token, (Operator, RParen)):
            raise InvalidExpressionError(f'Выражение не может начинаться с {token}')

    def _validate_last_token(self, token: Token) -> None:
        """Последний токен может заканчивать выражение"""
        if isinstance(token, (Operator, UnaryOperator, LParen)):
            raise InvalidExpressionError(f'Выражение не может заканчиваться на {token}')


class ExpressionEmptyValidator:
    """
    Выкидывает по ошибку при пустом списке токенов
    """

    def validate(self, tokens: List[Token]) -> None:
        if len(tokens) == 0:
            raise InvalidExpressionError('Список токенов пуст')
