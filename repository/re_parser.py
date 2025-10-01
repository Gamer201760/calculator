import re
from typing import Dict, List, Optional, Type

from domain.error import InvalidExpressionError, InvalidTokenError
from domain.operator import Add, Divide, IntegerDivide, Modulo, Multiply, Pow, Subtract
from domain.token import LParen, Number, Operator, RParen, Token, UnaryOperator
from domain.unary import UnaryMinus, UnaryPlus


class RegexTokenizer:
    """Токенизатор на регулярных выражениях"""

    def __init__(self) -> None:
        self._operators: Dict[str, Type[Operator]] = {
            '+': Add,
            '-': Subtract,
            '*': Multiply,
            '/': Divide,
            '^': Pow,
            '//': IntegerDivide,
            '%': Modulo,
        }
        self._unary: Dict[str, Type[UnaryOperator]] = {
            '-': UnaryMinus,
            '+': UnaryPlus,
        }

        self._pattern = re.compile(
            r'(?P<NUMBER>\d+\.?\d*)|'  # Числа
            # r'(?P<FUNCTION>sqrt|sin|cos|tan|log|abs|max|min)|'  # Функции
            # r'(?P<CONSTANT>tau|pi|e)|'  # Константы (tau первым для правильного распознавания)
            r'(?P<OPERATOR>//|[+\-*/^%])|'  # Операторы (// первым)
            r'(?P<LPAREN>\()|'  # Левая скобка
            r'(?P<RPAREN>\))|'  # Правая скобка
            # r'(?P<COMMA>,)|'  # Запятая
            r'(?P<WHITESPACE>\s+)|'  # Пробелы
            r'(?P<UNKNOWN>.)'  # Неизвестные символы
        )

    def _parse_operator(self, value: str, prev: Optional[Token]) -> Token:
        if isinstance(prev, UnaryOperator):
            raise InvalidExpressionError('После унарного опреатора, должно идти число')

        if (value in self._unary) and (
            prev is None or isinstance(prev, (Operator, LParen))
        ):
            return self._unary[value]()  # унарный оператор

        if prev is None:
            raise InvalidExpressionError('Бинарный оператор не может стоять первый')

        if isinstance(prev, Operator):
            raise InvalidExpressionError('После бинарного оператора, должно идти число')

        return self._operators[value]()

    def parse(self, expression: str) -> List[Token]:
        """Парсит выражение в список токенов"""
        tokens: List[Token] = []
        prev: Optional[Token] = None

        for match in self._pattern.finditer(expression):
            kind = match.lastgroup
            value = match.group()
            curr: Optional[Token] = None

            if kind == 'NUMBER':
                curr = Number(float(value))
            elif kind == 'OPERATOR':
                curr = self._parse_operator(value, prev)
            elif kind == 'LPAREN':
                curr = LParen()
            elif kind == 'RPAREN':
                curr = RParen()
            elif kind == 'WHITESPACE':
                # Игнорируем пробелы
                continue
            elif kind == 'UNKNOWN':
                raise InvalidTokenError(f'Неизвестный токен: "{value}"')

            if curr:
                tokens.append(curr)
                prev = curr

        if isinstance(
            tokens[-1], (Operator, UnaryOperator)
        ):  # Проверка последнего токена на бинарный, унарный оператор
            raise InvalidExpressionError(
                'Последний токен не может быть бинарным или унарным оператором'
            )

        return tokens
