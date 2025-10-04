import pytest

from domain.calculator import RPNCalculator
from domain.error import CalculationError
from domain.operator import Add, Divide, IntegerDivide, Modulo, Multiply, Pow, Subtract
from domain.token import Number
from domain.unary import UnaryMinus, UnaryPlus


@pytest.fixture
def calc() -> RPNCalculator:
    return RPNCalculator()


@pytest.mark.parametrize(
    'expr,expected',
    [
        # Сложение
        ((Number(2), Number(3), Add()), 5.0),
        ((Number(0), Number(0), Add()), 0.0),
        ((Number(-5), Number(3), Add()), -2.0),
        ((Number(1.5), Number(2.5), Add()), 4.0),
        # Вычитание
        ((Number(5), Number(3), Subtract()), 2.0),  # 5 - 3 = 2
        ((Number(3), Number(5), Subtract()), -2.0),  # 3 - 5 = -2
        ((Number(0), Number(5), Subtract()), -5.0),  # 0 - 5 = -5
        ((Number(2.5), Number(1.5), Subtract()), 1.0),  # 2.5 - 1.5 = 1.0
        # Умножение
        ((Number(3), Number(4), Multiply()), 12.0),
        ((Number(0), Number(5), Multiply()), 0.0),
        ((Number(-2), Number(3), Multiply()), -6.0),
        ((Number(1.5), Number(2.0), Multiply()), 3.0),
        # Деление
        ((Number(8), Number(2), Divide()), 4.0),  # 8 / 2 = 4
        ((Number(1), Number(4), Divide()), 0.25),  # 1 / 4 = 0.25
        ((Number(1.0), Number(0.5), Divide()), 2.0),  # 1.0 / 0.5 = 2.0
        # Возведение в степень
        ((Number(3), Number(2), Pow()), 9.0),  # 3^2 = 9
        ((Number(2), Number(3), Pow()), 8.0),  # 2^3 = 8
        ((Number(5), Number(0), Pow()), 1.0),  # 5^0 = 1
        ((Number(0.5), Number(2), Pow()), 0.25),  # 0.5^2 = 0.25
    ],
)
def test_binary_operations(calc, expr, expected):
    assert calc.calculate(expr) == pytest.approx(expected)


@pytest.mark.parametrize(
    'expr,expected',
    [
        # Унарный минус
        ((Number(5), UnaryMinus()), -5.0),
        ((Number(-3), UnaryMinus()), 3.0),
        ((Number(0), UnaryMinus()), 0.0),
        ((Number(2.5), UnaryMinus()), -2.5),
        # Унарный плюс
        ((Number(5), UnaryPlus()), 5.0),
        ((Number(-3), UnaryPlus()), -3.0),
        ((Number(0), UnaryPlus()), 0.0),
        ((Number(2.5), UnaryPlus()), 2.5),
    ],
)
def test_unary_operations(calc, expr, expected):
    assert calc.calculate(expr) == pytest.approx(expected)


@pytest.mark.parametrize(
    'expr,expected',
    [
        ((Number(2), Number(2), UnaryMinus(), Add()), 0.0),
        ((Number(2), Number(2), UnaryMinus(), Subtract()), 4.0),
        ((Number(3), UnaryMinus(), Number(2), Add()), -1.0),
        ((Number(2), Number(3), Add(), Number(4), Multiply()), 20.0),
        ((Number(10), Number(2), Divide(), Number(3), Add()), 8.0),
        ((Number(2), Number(3), Pow(), Number(1), Add()), 9.0),
        ((Number(1), Number(2), Add(), Number(3), Add(), Number(4), Add()), 10.0),
        (
            (Number(2), Number(3), Multiply(), Number(4), Number(5), Multiply(), Add()),
            26.0,
        ),
        ((Number(5), Number(3), UnaryMinus(), Number(2), Add(), Subtract()), 6.0),
    ],
)
def test_complex_expressions(calc, expr, expected):
    assert calc.calculate(expr) == pytest.approx(expected)


@pytest.mark.parametrize(
    'expr,expected',
    [
        ((Number(10), Number(3), IntegerDivide()), 3.0),
        ((Number(12), Number(4), IntegerDivide()), 3.0),
        ((Number(7), Number(5), IntegerDivide()), 1.0),
        ((Number(1), Number(2), IntegerDivide()), 0.0),
        ((Number(10), Number(3), Modulo()), 1.0),
        ((Number(12), Number(4), Modulo()), 0.0),
        ((Number(7), Number(5), Modulo()), 2.0),
        ((Number(1), Number(2), Modulo()), 1.0),
    ],
)
def test_integer_operations(calc, expr, expected):
    assert calc.calculate(expr) == pytest.approx(expected)


@pytest.mark.parametrize(
    'expr,expected',
    [
        ((Number(0), Number(5), Add()), 5.0),
        ((Number(5), Number(0), Add()), 5.0),
        ((Number(0), Number(0), Add()), 0.0),
        ((Number(0), Number(5), Multiply()), 0.0),
        ((Number(5), Number(0), Multiply()), 0.0),
        ((Number(1), Number(0), Pow()), 1.0),  # 1^0 = 1
        ((Number(5), Number(1), Pow()), 5.0),  # 5^1 = 5
        ((Number(1), Number(2), Pow()), 1.0),  # 1^2 = 1
        ((Number(2), Number(-1), Pow()), 0.5),  # 2^(-1) = 0.5
        ((Number(4), Number(-2), Pow()), 0.0625),  # 4^(-2) = 0.0625
        ((Number(0.1), Number(0.2), Add()), 0.3),
        ((Number(1.5), Number(2.5), Multiply()), 3.75),
    ],
)
def test_edge_cases(calc, expr, expected):
    assert calc.calculate(expr) == pytest.approx(expected, rel=1e-9)


@pytest.mark.parametrize(
    'expr,expected',
    [
        ((Number(1e10), Number(1e10), Add()), 2e10),
        ((Number(1e10), Number(2), Multiply()), 2e10),
        ((Number(1e-10), Number(1e-10), Add()), 2e-10),
        ((Number(1e-5), Number(1e-5), Multiply()), 1e-10),
        ((Number(-5), Number(-3), Add()), -8.0),
        ((Number(-5), Number(-3), Multiply()), 15.0),
        ((Number(-8), Number(-2), Divide()), 4.0),  # -8 / -2 = 4
    ],
)
def test_special_values(calc, expr, expected):
    assert calc.calculate(expr) == pytest.approx(expected, rel=1e-9)


@pytest.mark.parametrize(
    'expr',
    [
        (Number(1e10), Number(1e10), Pow()),
    ],
)
def test_calculation_error(calc, expr):
    with pytest.raises(CalculationError):
        calc.calculate(expr)
