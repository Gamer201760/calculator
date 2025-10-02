from typing import Optional

from domain.calculator import RPNCalculator
from usecase.interface import (
    ProcessorInterface,
    RPNConverterInterface,
    TokenizerInterface,
    ValidatorInterface,
)


class InfixCalculatorUsecase:
    def __init__(
        self,
        tokenizer: TokenizerInterface,
        calculator: RPNCalculator,
        conveter: RPNConverterInterface,
        processor: ProcessorInterface,
        validator: Optional[ValidatorInterface] = None,
    ):
        self._tokenizer = tokenizer
        self._validator = validator
        self._conveter = conveter
        self._processor = processor
        self._calculator = calculator

    def exec(self, expr: str) -> float:
        tokens = self._tokenizer.parse(expr)
        # TODO: add validator after parse
        tokens = self._processor.process(tokens)
        tokens = self._conveter.convert(tokens)
        if self._validator:
            self._validator.validate(tokens)

        return self._calculator.calculate(tokens)
