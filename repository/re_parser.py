import re
from typing import Dict, List, Type

from domain.error import InvalidTokenError
from domain.operator import Add, Divide, IntegerDivide, Modulo, Multiply, Pow, Subtract
from domain.token import LParen, Number, Operator, RParen, Token, UnaryOperator
from domain.unary import UnaryMinus, UnaryPlus


class RegexTokenizer:
    """
    Токенизатор на регулярных выражениях,
    просто преобразует строку в токены,
    никаких проверок не выполняет
    """

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
        self._unary_ops: Dict[str, Type[UnaryOperator]] = {
            '~': UnaryMinus,
            '$': UnaryPlus,
        }

        self._pattern = re.compile(
            r'(?P<NUMBER>\d+\.?\d*)|'  # Числа
            # r'(?P<FUNCTION>sqrt|sin|cos|tan|log|abs|max|min)|'  # Функции
            # r'(?P<CONSTANT>tau|pi|e)|'  # Константы (tau первым для правильного распознавания)
            r'(?P<OPERATOR>//|[+\-*/^%])|'  # Операторы (// первым)
            r'(?P<UNARY_OPERATOR>[~$])|'  # Унарные операторы
            r'(?P<LPAREN>\()|'  # Левая скобка
            r'(?P<RPAREN>\))|'  # Правая скобка
            # r'(?P<COMMA>,)|'  # Запятая
            r'(?P<WHITESPACE>\s+)|'  # Пробелы
            r'(?P<UNKNOWN>.)'  # Неизвестные символы
        )

    def parse(self, expression: str) -> List[Token]:
        """Парсит выражение в список токенов"""
        tokens: List[Token] = []

        for match in self._pattern.finditer(expression):
            kind = match.lastgroup
            value = match.group()

            if kind == 'NUMBER':
                tokens.append(Number(float(value)))
            elif kind == 'OPERATOR':
                tokens.append(self._operators[value]())
            elif kind == 'UNARY_OPERATOR':
                tokens.append(self._unary_ops[value]())
            elif kind == 'LPAREN':
                tokens.append(LParen())
            elif kind == 'RPAREN':
                tokens.append(RParen())
            elif kind == 'WHITESPACE':
                # Игнорируем пробелы
                continue
            elif kind == 'UNKNOWN':
                raise InvalidTokenError(f'Неизвестный токен: "{value}"')
        return tokens
