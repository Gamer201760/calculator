from typing import List, Optional

from usecase.interface import (
    RPNCalculatorInterface,
    RPNConverterInterface,
    TokenizerInterface,
    ValidatorInterface,
)


class RPNCalculatorUseCase:
    """Use case для вычисления RPN выражений"""

    def __init__(
        self,
        parser: TokenizerInterface,
        converter: RPNConverterInterface,
        calc: RPNCalculatorInterface,
        validators: Optional[List[ValidatorInterface]] = None,
    ):
        self._parser = parser
        self._converter = converter
        self._calc = calc
        self._validators = validators

    def calculate(self, expression: str) -> float:
        """Вычисляет RPN выражение"""
        tokens = self._parser.parse(expression)
        if self._validators:
            for validator in self._validators:
                validator.validate(tokens)
        tokens = self._converter.convert(tokens)
        return self._calc.calculate(tokens)
