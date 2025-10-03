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
        pre_validator: Optional[ValidatorInterface] = None,
        post_validator: Optional[ValidatorInterface] = None,
    ):
        self._tokenizer = tokenizer
        self._conveter = conveter
        self._processor = processor
        self._calculator = calculator
        self._pre_validator = pre_validator
        self._post_validator = post_validator

    def exec(self, expr: str) -> float:
        tokens = self._tokenizer.parse(expr)
        tokens = self._processor.process(tokens)

        if self._pre_validator:
            self._pre_validator.validate(tokens)

        tokens = self._conveter.convert(tokens)
        if self._post_validator:
            self._post_validator.validate(tokens)

        return self._calculator.calculate(tokens)
