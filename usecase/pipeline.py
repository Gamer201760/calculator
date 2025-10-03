from typing import List, Protocol

from domain.token import Token
from usecase.interface import (
    ProcessorInterface,
    RPNConverterInterface,
    ValidatorInterface,
)


class PipelineStepInterface(Protocol):
    """
    Интерфейс шага в конвейере обработки токенов
    """

    def process(self, tokens: List[Token]) -> List[Token]: ...


class ValidationStep(PipelineStepInterface):
    """Шаг конвейера для валидатора"""

    def __init__(self, validator: ValidatorInterface) -> None:
        self._validator = validator

    def process(self, tokens: List[Token]) -> List[Token]:
        self._validator.validate(tokens)
        return tokens


class ProcessingStep(PipelineStepInterface):
    """Шаг конвейера для обработки токенов"""

    def __init__(self, processor: ProcessorInterface) -> None:
        self._processor = processor

    def process(self, tokens: List[Token]) -> List[Token]:
        return self._processor.process(tokens)


class ConversionStep(PipelineStepInterface):
    """Шаг конвейера для конвертации токенов"""

    def __init__(self, converter: RPNConverterInterface) -> None:
        self._converter = converter

    def process(self, tokens: List[Token]) -> List[Token]:
        return self._converter.convert(tokens)
