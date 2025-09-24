from random import randint

import pytest

from domain.operator import Add, Divide, IntegerDivide, Modulo, Multiply, Pow, Subtract
from domain.token import Operator


def test_symbol_add():
    add = Add()
    assert add.symbol == '+'


def test_symbol_sub():
    sub = Subtract()
    assert sub.symbol == '-'


def test_symbol_div():
    div = Divide()
    assert div.symbol == '/'


def test_symbol_mul():
    mul = Multiply()
    assert mul.symbol == '*'


def test_symbol_pow():
    pow = Pow()
    assert pow.symbol == '^'


def test_symbol_integer_div():
    div = IntegerDivide()
    assert div.symbol == '//'


def test_symbol_modulo():
    mod = Modulo()
    assert mod.symbol == '%'


def test_add():
    add = Add()
    a = randint(0, 100000) / 100
    b = randint(0, 100000) / 100

    assert add.execute(a, b) == a + b


def test_sub():
    sub = Subtract()
    a = randint(0, 100000) / 100
    b = randint(0, 100000) / 100

    assert sub.execute(a, b) == b - a


def test_div():
    div = Divide()
    a = randint(1, 100000) / 100
    b = randint(1, 100000) / 100

    assert div.execute(a, b) == b / a


def test_div_zero():
    div = Divide()
    a = 0
    b = randint(1, 100000) / 100

    with pytest.raises(ValueError):
        div.execute(a, b)


def test_mul():
    mul = Multiply()
    a = randint(0, 100000) / 100
    b = randint(0, 100000) / 100

    assert mul.execute(a, b) == a * b


def test_pow():
    pow = Pow()
    a = randint(0, 10000) / 100
    b = randint(0, 10000) / 100

    assert pow.execute(a, b) == b**a


def test_integer_div():
    div = IntegerDivide()
    a = randint(0, 100000)
    b = randint(0, 100000)

    assert div.execute(a, b) == b // a


def test_modulo():
    mod = Modulo()
    a = randint(0, 100000)
    b = randint(0, 100000)

    assert mod.execute(a, b) == b % a


def test_op():
    class Op(Operator):
        def execute(self, a: float, b: float) -> float:
            return a + b

    op = Op()
    print(op.symbol)
