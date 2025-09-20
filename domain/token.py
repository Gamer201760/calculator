from dataclasses import dataclass
from enum import Enum
from typing import Union


class TokenType(Enum):
    NUMBER = 'NUMBER'
    OPERATOR = 'OPERATOR'


@dataclass
class Token:
    type: TokenType
    value: Union[float, str]
