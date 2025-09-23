from random import randint

import pytest

from domain.operator import Add, Divide, Multiply, Pow, Subtract


def test_symbol_add():
    add = Add()
    assert add.get_symbol() == '+'


def test_symbol_sub():
    sub = Subtract()
    assert sub.get_symbol() == '-'


def test_symbol_div():
    div = Divide()
    assert div.get_symbol() == '/'


def test_symbol_mul():
    mul = Multiply()
    assert mul.get_symbol() == '*'


def test_symbol_pow():
    pow = Pow()
    assert pow.get_symbol() == '^'


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
    a = randint(0, 100000) / 100
    b = randint(0, 100000) / 100

    assert pow.execute(a, b) == a**b
