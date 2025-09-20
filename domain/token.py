from dataclasses import dataclass
from typing import Union
from enum import Enum


class TokenType(Enum):
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"


@dataclass
class Token:
    type: TokenType
    value: Union[float, str]
