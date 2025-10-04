class DomainError(Exception):
    """Базовый класс для всех внутренних ошибок"""


class InvalidTokenError(DomainError):
    """Неизвестный токен"""


class InvalidExpressionError(DomainError):
    """Некорректное выражение"""


class InsufficientOperandsError(DomainError):
    """Нехватка операндов для выполнения операции"""


class CalculationError(DomainError):
    """Вычислительная ошибка"""
