from typing import List, Optional

from domain.calculator import RPNCalculator
from domain.token import LParen, RParen, Token
from usecase.interface import TokenizerInterface, ValidatorInterface


class RPNCalculatorUsecase:
    def __init__(
        self,
        tokenizer: TokenizerInterface,
        calculator: RPNCalculator,
        validators: Optional[List[ValidatorInterface]] = None,
    ):
        self._tokenizer = tokenizer
        self._validators = validators
        self._calculator = calculator

    def _remove_paren(self, tokens: List[Token]) -> List[Token]:
        return [token for token in tokens if not isinstance(token, (LParen, RParen))]

    def exec(self, expr: str) -> float:
        tokens = self._tokenizer.parse(expr)

        if self._validators:
            for validator in self._validators:
                validator.validate(tokens)

        return self._calculator.calculate(self._remove_paren(tokens))
