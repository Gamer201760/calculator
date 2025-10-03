from typing import List

from domain.calculator import RPNCalculator
from usecase.interface import TokenizerInterface
from usecase.pipeline import PipelineStepInterface


class CalculatorUsecase:
    def __init__(
        self,
        tokenizer: TokenizerInterface,
        pipeline: List[PipelineStepInterface],
        calculator: RPNCalculator,
    ):
        self._tokenizer = tokenizer
        self._pipeline = pipeline
        self._calculator = calculator

    def exec(self, expr: str) -> float:
        tokens = self._tokenizer.parse(expr)

        for step in self._pipeline:
            tokens = step.process(tokens)

        return self._calculator.calculate(tokens)
